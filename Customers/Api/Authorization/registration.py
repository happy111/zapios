from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from ZapioApi.api_packages import *
from rest_framework_tracking.mixins import LoggingMixin

# For emailing
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from _thread import start_new_thread
from django.db.models import Q
from Customers.notification.notification_email_service import (
    EmailNotifications,
    SMSNotifications,
)
from Customers.serializers.customer_serializer import (
    CustomerSignUpSerializer,
    CustomerOTPSerializer,
)

from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy

def otp_email_notification(customerId, eotp, motp, services):
    email_notification_instance = EmailNotifications(
        customer_id=customerId,
        otp=eotp,
        motp=motp,
        api_name=services,
        email_html_template="emailer/activation_mail.html",
    )
    email_notification_instance()


def otp_sms_notification(customerId, motp, services):
    sms_notification_instance = SMSNotifications(
        customer_id=customerId, motp=motp, api_name=services
    )
    sms_notification_instance()


class CustomerRegistration(LoggingMixin, APIView):
    """
    Customer Registration POST API

        Authentication Required     : No
        Service Usage & Description : This Api is used to customer Registration
        {
            "email": "umeshsamal3@gmail.com",
            "mobile": "8750477098",
            "pass_pin": "123456",
            "name" : "no name",
            "company" : "3",
        }
        Response: {
            "success": True,
            "customer_id" : 125,
            "message": "You have been registered successfully..A confirmation OTP has been sent on your email id!!"
        }

    """

    def post(self, request, format=None):
        try:
            registration_data = request.data
            err_message = {}
            otp_data = {}
            err_message["email"] = validation_master_anything(
                registration_data["email"], "Email", email_re, 3
            )
            err_message["password"] = validation_master_exact(
                registration_data["pass_pin"], "Password", contact_re, 6
            )
            err_message["mobile"] = validation_master_exact(
                registration_data["mobile"], "Mobile No.", contact_re, 10
            )
            if any(err_message.values()) == True:
                return Response(
                    {"error": err_message, "message": "Please correct listed errors!!"}
                )
            username = str(registration_data["company"]) + registration_data["mobile"]
            user_already_exist = User.objects.filter(username=username)
            if user_already_exist.count() == 1:
                return Response(
                    {
                        "success": False,
                        "message": gettext_lazy("User with the entered mobile number already"
                        " exists..Please login directly!!"),
                    }
                )
            email = str(registration_data["company"]) + registration_data["email"]
            email_already_exist = User.objects.filter(email=email)
            if email_already_exist.count() == 1:
                return Response(
                    {
                        "success": False,
                        "message": gettext_lazy("User with the entered email already exists..Please login directly!!"),
                    }
                )
            create_user = User.objects.create_user(
                username=username,
                email=email,
                password=registration_data["pass_pin"],
                is_staff=False,
                is_active=True,
            )
            if create_user:
                registration_data["auth_user"] = create_user.id
                # registration_data["name"] = "No Name"
                registration_data["username"] = registration_data["mobile"]
                customer_registration_serializer = CustomerSignUpSerializer(
                    data=registration_data
                )
                if customer_registration_serializer.is_valid():
                    customer_data_save = customer_registration_serializer.save()
                    otp_data["customer"] = customer_data_save.id
                    otp_data["email_OTP"] = otp_generator()
                    otp_data["mobile_OTP"] = otp_generator()
                    otp_serializer = CustomerOTPSerializer(data=otp_data)
                    if otp_serializer.is_valid():
                        otp_serializer.save()
                    else:
                        return Response(
                            {"success": False, "otp_error": str(otp_serializer.errors),}
                        )
                    confirmation_context = {"email_OTP": otp_data["email_OTP"]}
                    to_email = registration_data["email"]
                    emailer_page = "emailer/activation_mail.html"
                    mail_subject = "Activate your zapio account"
                    services = "__registrationotpit__"
                    customerId = otp_serializer.data["customer"]
                    eotp = otp_data["email_OTP"]
                    motp = otp_data["mobile_OTP"]
                    start_new_thread(
                        otp_email_notification, (customerId, eotp, motp, services)
                    )
                    start_new_thread(otp_sms_notification, (customerId, motp, services))
                    return Response(
                        {
                            "success": True,
                            "message": gettext_lazy("You have been registered successfully..A confirmation OTP has been sent on your email id and mobile number!!"),
                            "customer_id": customer_data_save.id,
                        }
                    )
                else:
                    return Response(
                        {
                            "success": False,
                            "message": str(customer_registration_serializer.errors),
                        }
                    )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Some error occured in the process of user creation!!",
                    }
                )
        except Exception as e:
            print("Registration Api Stucked into exception!!")
            print(e)
            return Response(
                {"success": False, "message": "Error happened!!", "errors": str(e)}
            )


class OtpVerificationemail(LoggingMixin, APIView):
    """
    This APi used both email and mobile verify

        Authentication Required     : No
        Post Data: {
            "customer_id" : "12",
            "email_OTP" : "X52PLQF"
        }
        Response: {
            "success": True,
            "customer_id" : 12,
            "message": "You email has been verified successfully!!"
        }

    """

    def post(self, request, format=None):
        try:
            from Customers.models import customer_otp, CustomerProfile

            otp_data = request.data
            err_message = {}
            mob_data = {}
            err_message["customer_id"] = validation_master_anything(
                otp_data["customer_id"], "Custoemr ID", contact_re, 1
            )
            err_message["email_OTP"] = validation_master_anything(
                otp_data["email_OTP"], "OTP", vat_re, 4
            )
            if any(err_message.values()) == True:
                return Response(
                    {
                        "success": False,
                        "error": err_message,
                        "message": "Please correct listed errors!!",
                    }
                )
            otp_data["customer"] = int(otp_data["customer_id"])
            valid_otp = customer_otp.objects.filter(customer_id=otp_data["customer"])
            is_email_otp_used = valid_otp.filter(
                Q(is_email_otp_used=1) & Q(email_OTP=otp_data["email_OTP"])
            )
            if is_email_otp_used.count() == 1:
                return Response(
                    {
                        "success": True,
                        "customer_id": otp_data["customer"],
                        "message": "The entered Email OTP is expired!!",
                    }
                )
            is_mobile_otp_used = valid_otp.filter(
                Q(is_mob_otp_used=1) & Q(mobile_OTP=otp_data["email_OTP"])
            )
            if is_mobile_otp_used.count() == 1:
                return Response(
                    {
                        "success": True,
                        "customer_id": otp_data["customer"],
                        "message": gettext_lazy("The entered mobile OTP is expired!!"),
                    }
                )

            customer_data = CustomerProfile.objects.filter(id=otp_data["customer"])
            if valid_otp.count() == 1 and customer_data.count() == 1:
                if valid_otp[0].email_OTP == otp_data["email_OTP"]:
                    otp_data["is_email_verfied"] = 1
                    otp_data["active_status"] = 1
                    otp_data["is_email_otp_used"] = 1
                    otp_serializer = CustomerOTPSerializer(
                        valid_otp[0], data=otp_data, partial=True
                    )
                    customer_serializer = CustomerSignUpSerializer(
                        customer_data[0], data=otp_data, partial=True
                    )
                    if otp_serializer.is_valid() and customer_serializer.is_valid():
                        otp_serializer.save()
                        customer_serializer.save()
                    else:
                        return Response(
                            {
                                "success": False,
                                "customer_error": str(customer_serializer.errors),
                                "otp_error": str(otp_serializer.errors),
                            }
                        )
                    return Response(
                        {
                            "success": True,
                            "customer_id": otp_data["customer"],
                            "message": gettext_lazy("Your email has been successfully verified!!"),
                        }
                    )
                if valid_otp[0].mobile_OTP == otp_data["email_OTP"]:
                    mob_data["is_mobile_verified"] = 1
                    mob_data["active_status"] = 1
                    mob_data["is_mob_otp_used"] = 1
                    mob_data["customer"] = int(otp_data["customer_id"])
                    mob_data["mobile_OTP"] = otp_data["email_OTP"]
                    otp_serializer = CustomerOTPSerializer(
                        valid_otp[0], data=mob_data, partial=True
                    )
                    customer_serializer = CustomerSignUpSerializer(
                        customer_data[0], data=mob_data, partial=True
                    )
                    if otp_serializer.is_valid() and customer_serializer.is_valid():
                        otp_serializer.save()
                        customer_serializer.save()
                    else:
                        return Response(
                            {
                                "success": False,
                                "customer_error": str(customer_serializer.errors),
                                "otp_error": str(otp_serializer.errors),
                            }
                        )
                    return Response(
                        {
                            "success": True,
                            "customer_id": otp_data["customer"],
                            "message": gettext_lazy("Your mobile has been successfully verified!!"),
                        }
                    )
                else:
                    return Response(
                        {
                            "success": False,
                            "message": "OTP entered by you is not correct!!",
                        }
                    )
            else:
                return Response(
                    {"success": False, "message": "Data is not consistent!!"}
                )
        except Exception as e:
            print("OTP Api Stucked into exception!!")
            print(e)
            return Response(
                {"success": False, "message": "Error happened!!", "errors": str(e)}
            )
