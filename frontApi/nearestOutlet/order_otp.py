import math
import json
import datetime
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from frontApi.serializer.customer_serializers import CustomerSignUpSerializer
from rest_framework_tracking.mixins import LoggingMixin
from _thread import start_new_thread
# from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from ZapioApi.api_packages import *
from Notification.models import EmailVerify
from Brands.models import Company
from email_validator import validate_email, EmailNotValidError
from Customers.models import CustomerProfile





def email_send_module(post_data):
    try:
        to = post_data["email"].lower()
        cname = Company.objects.filter(id=post_data['Company'])[0]
        if cname.company_logo != None:
            domain_name = addr_set()
            full_path = domain_name + str(cname.company_logo)
        else:
            full_path = ''
        cc_email_id = []
        to_email = [
            to,
        ]
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {'Content-type': 'application/json',
            "Authorization": "Bearer ",
           'Accept': 'application/json'}
        data = {
              "personalizations": [
                {
                  "to": [
                    {
                      "email": to,
                    },

                  ],
                  "dynamic_template_data": {
                  "company_name":cname.company_name,
                  "name":post_data['name'],
                  "otp" : post_data['otp'],
                  "logo" :full_path.strip()
 
                },
                }
              ],
              "from": {
                "email": "umeshsamal070@gmail.com",
                "name" : cname.company_name
              },
                "subject": "mail_subject",
                "template_id":"d-7fe20c18c4924925b8df961f9494bbc5",
                "content": [{"type": "text/html", "value": "Heya!"}]
            }
        response= requests.post(url,data=json.dumps(data),headers=headers)
        return response
    except Exception as e:
        print(e)


def otp_generator():
    import random
    otp = random.randint(1000, 9999)
    return otp


class EmailOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerify
        fields = '__all__'


class OrderOtp(LoggingMixin, APIView):

    """
    send otp POST API

        Authentication Required     : No
        Service Usage & Description : This Api is used to send otp.

        Data Post:  {
                "name"  : ""
                "email" : "umesh@eoraa.com"
                "company" : ""
              }

        Response: {

            "success": true,
            "message": "Email Verify successfully"
        }

    """

    def post(self, request, format=None):
        try:
            post_data = request.data
            err_message = {}
            flag = 0
            try:
                valid = validate_email(post_data["email"].lower())  
            except EmailNotValidError as e:
                return Response(
                        {
                            "success": False, 
                        })
            if post_data['forget'] == 1:
                email_data = EmailVerify.objects.filter(email=post_data["email"].lower(),Company_id=post_data['Company'],\
                    active_status=1)
                if email_data.count() > 0:
                    temp = {}
                    temp["otp"]  = otp_generator()
                    temp['otp_creation_time'] =  datetime.now()
                    temp['active_status'] = 0
                    temp['types'] = 'Online'
                    temp['name'] = email_data[0].name
                    temp['email'] = email_data[0].email
                    temp['Company'] = email_data[0].Company_id
                    otp_serializer = EmailOTPSerializer(email_data[0],data=temp,partial=True)
                    if otp_serializer.is_valid():
                        otp_serializer.save()
                        res = start_new_thread(email_send_module, (temp,))
                        email_data = EmailVerify.objects.filter(email=post_data['email'],Company_id=post_data['Company'],\
                            active_status=0)
                        return Response(
                            {
                                "success": True, 
                                "message": "OTP is send successfully",
                                "email_status" : False,
                                "name" : email_data[0].name,
                                "email" : email_data[0].email
                            })
                    else:
                        pass
            if flag == 0:
                email_data = EmailVerify.objects.filter(email=post_data["email"].lower(),Company_id=post_data['Company'],\
                    active_status=1,types='Online')
                cus_data = CustomerProfile.objects.filter(email=post_data["email"].lower(),company_id=post_data['Company'],is_google=1)
                if email_data.count() > 0 or cus_data.count() > 0:
                    cus_data = CustomerProfile.objects.filter(email=post_data["email"].lower(),company_id=post_data['Company'])
                    final_result = []
                    if cus_data.count() > 0:
                        adress_data = cus_data[0].address1
                        if adress_data != None and len(adress_data) > 0:
                            for k in adress_data:
                                di = {}
                                try:
                                    if cus_data[0].name != None:
                                        di['first_name'] = cus_data[0].name.split(' ')[0]
                                        if len(cus_data[0].name.split(' ')) >= 2:
                                            di['last_name'] = cus_data[0].name.split(' ')[1]
                                        else:
                                            di['last_name'] = ''
                                except Exception as e:
                                    print(e)
                                di['email'] = cus_data[0].email
                                di['phone'] = cus_data[0].mobile
                                if 'city' in k:
                                    di['city']  = k['city']
                                else:
                                    di['city'] = ''
                                if 'state' in k:
                                    di['state']  = k['state']
                                else:
                                    di['state'] = ''
                                if 'address' in k:
                                    di['address'] = k['address']
                                else:
                                    di['address'] = ''
                                
                                if 'pincode' in k:
                                    di['pincode'] = k['pincode']
                                else:
                                    di['pincode'] = ''
                                di['locality'] = k['locality']
                                di['address_type'] = k['address_type']
                                final_result.append(di)
                    if len(final_result) > 0:
                        pass
                    else:
                        cus_data = CustomerProfile.objects.filter(email=post_data["email"].lower(),company_id=post_data['Company'],is_google=1)
                        if cus_data.count() > 0:
                            name = cus_data[0].name
                            di={}
                            di['first_name'] = name.split(' ')[0]
                            di['last_name']      = name.split(' ')[1]
                            di['email'] = post_data['email']
                            final_result.append(di)
                        else:
                            di={}
                            di['first_name'] = email_data[0].name
                            di['email']      = email_data[0].email
                            final_result.append(di)
                    return Response(
                        {
                            "success": True, 
                            "message": "Already Verified!!",
                            "email_status" : True,
                            "data" : final_result,
                        })
                email_dt = EmailVerify.objects.filter(email=post_data["email"].lower(),Company_id=post_data['Company'],\
                    active_status=0,types='Online')
                if email_dt.count() > 0:
                    temp = {}
                    temp["otp"] = otp_generator()
                    temp['otp_creation_time'] =  datetime.now()
                    temp['active_status'] = 0
                    temp['types'] = 'Online'
                    temp['name'] = email_dt[0].name
                    temp['email'] = email_dt[0].email
                    temp['Company'] = email_dt[0].Company_id
                    otp_serializer = EmailOTPSerializer(email_dt[0],data=temp,partial=True)
                    if otp_serializer.is_valid():
                        otp_serializer.save()
                        res = start_new_thread(email_send_module, (temp,))
                        return Response(
                            {
                                "success": True, 
                                "message": "OTP is send successfully",
                                "email_status" : False,
                                "name" : email_dt[0].name,
                                "email" : email_dt[0].email
                            })
                    else:
                        return Response(
                            {
                                "success": False, 
                                "message": otp_serializer.errors
                            })
                else:
                    post_data["otp"] = otp_generator()
                    post_data['otp_creation_time'] =  datetime.now()
                    post_data['types'] = 'Online'
                    otp_serializer = EmailOTPSerializer(data=post_data)
                    if otp_serializer.is_valid():
                        otp_serializer.save()
                        res = start_new_thread(email_send_module, (post_data,))
                        return Response(
                            {
                                "success": True, 
                                "message": "OTP is send successfully",
                                "email_status" : False,
                                "name" : post_data['name'],
                                "email" : post_data['email']
                            })
                    else:
                        return Response(
                            {
                                "success": False, 
                                "message": otp_serializer.errors
                            })
            else:
                return Response(
                        {
                            "success": False, 
                        })

        except Exception as e:
            print(e)
            return Response(
                {
                    "success": False,
                    "message": "Email Verify api stucked into exception!!",
                }
            )



class VerifyOtp(LoggingMixin, APIView):

    """
    Customer Email verify POST API

        Authentication Required     : No
        Service Usage & Description : This Api is used to email verify.

        Data Post:  {
                
                "email" : "umesh@eoraa.com"
                "otp"   : ""
                "Company" : ""
              }

        Response: {

            "success": true,
            "message": "Email Verify successfully"
        }

    """

    def post(self, request, format=None):
        try:
            post_data = request.data
            err_message = {}
            err_message["email"] = validation_master_anything(
                post_data["email"].lower(), "Email", email_re, 3
            )
            if any(err_message.values())==True:
                return Response({
                    "success"   : False,
                    "error"     : err_message,
                    "message"   : "Please correct listed errors!!"
                    })

            email_data = EmailVerify.objects.filter(email=post_data["email"].lower(),\
                otp=post_data['otp'],active_status=0,\
                Company_id=post_data['Company'],types='Online')
            if email_data.count() > 0:
                post_data['otp_use_time'] =  datetime.now()
                otp_serializer = EmailOTPSerializer(email_data[0],data=post_data,partial=True)
                if otp_serializer.is_valid():
                    otp_serializer.save()
                    email_dt = EmailVerify.objects.filter(email=post_data["email"].lower(),\
                        otp=post_data['otp'],Company_id=post_data['Company'])
                    link_create_time = email_dt.first().otp_creation_time
                    link_used_time = email_dt.first().otp_use_time
                    time_diff = link_used_time-link_create_time
                    get_minutes = time_diff.total_seconds() / 60
                    expire_msg = "Your otp has been expired..please generate again!!"
                    if get_minutes > 100:
                        email_data.delete()
                        return Response({
                                    "status": False,
                                    "message": expire_msg
                                    })
                    else:
                        post_data['name'] = email_data[0].name
                        email_data.update(active_status=1)
                        email_data = EmailVerify.objects.filter(email=post_data["email"].lower(),Company_id=post_data['Company'],\
                            active_status=1)
                        if email_data.count() > 0:
                            cus_data = CustomerProfile.objects.filter(email=post_data["email"].lower(),company_id=post_data['Company'])
                            final_result = []
                            if cus_data.count() > 0:
                                adress_data = cus_data[0].address1
                                if adress_data != None and len(adress_data) > 0:
                                    for k in adress_data:
                                        di = {}
                                        if cus_data[0].name != None:
                                            di['first_name'] = cus_data[0].name.split(' ')[0]
                                            if len(cus_data[0].name.split(' ')) >= 2:
                                                di['last_name'] = cus_data[0].name.split(' ')[1]
                                            else:
                                                di['last_name'] = ''
                                        di['email']  = cus_data[0].email
                                        di['phone']  = cus_data[0].mobile
                                        if 'city' in k:
                                            di['city']  = k['city']
                                        else:
                                            di['city'] = ''
                                        if 'state' in k:
                                            di['state']  = k['state']
                                        else:
                                            di['state'] = ''
                                        if 'address' in k:
                                            di['address'] = k['address']
                                        else:
                                            di['address'] = ''
                                        if 'pincode' in k:
                                            di['pincode'] = k['pincode']
                                        else:
                                            di['pincode'] = ''
                                        di['locality'] = k['locality']
                                        di['address_type'] = k['address_type']
                                        final_result.append(di)
                            else:
                                pass
                            return Response({
                                        "status": True,
                                        "message": "Verify Successfully!!",
                                        "data" : final_result
                                        })
            else:
                return Response({
                                    "status": False,
                                    "message": "The OTP entered by you is incorrect. Please enter the correct OTP and try again."
                                })
        except Exception as e:
            print(e)
            return Response(
                {
                    "success": False,
                    "message": "Email Verify api stucked into exception!!",
                }
            )





class MphinOtp(LoggingMixin, APIView):

    """
    MPHIN Create POST API

        Authentication Required     : No
        Service Usage & Description : This Api is used to create mphin.

        Data Post:  {
                
                "email"   : ""
                "mpin"    : "3456"
                "cmpin"   : ""

              }

        Response: {

            "success": true,
            "message": "m successfully"
        }

    """

    def post(self, request, format=None):
        try:
            data = request.data
            err_message = {}
            if data["mpin"]!=data["cmpin"]:
                err_message["c_pwd"] = "MPIN and ReMPIN doesn't match!!"
            if any(err_message.values())==True:
                return Response({
                    "success"   : False,
                    "error"     : err_message,
                    "message"   : "Please correct listed errors!!"
                    })
            email_data = EmailVerify.objects.filter(email=data['email'].lower(),\
                active_status=1,Company_id=data['Company'],types='Online')
            if email_data.count() > 0:
                email_data.update(active_status=1,mphin=data['mpin'])
                return Response({
                            "status"  : True,
                            "message" : "MPIN created successfully!!",
                            })
            else:
                return Response({
                                    "status"  : False,
                                    "message" : "Error occured!!"
                                })
        except Exception as e:
            print(e)
            return Response(
                {
                    "success": False,
                    "message": "Api stucked into exception!!",
                }
            )





class VerifyMpin(LoggingMixin, APIView):

    """
    Customer MPIN verify POST API

        Authentication Required     : No
        Service Usage & Description : This Api is used to MPIN verify.

        Data Post:  {
                
                "email" : "umesh@eoraa.com"
                "mpin"   : ""
                "Company" : ""
              }

        Response: {

            "success": true,
            "message": "MPIN Verify successfully"
        }

    """

    def post(self, request, format=None):
        try:
            post_data = request.data
            err_message = {}
            err_message["email"] = validation_master_anything(
                post_data["email"].lower(), "Email", email_re, 3
            )
            if any(err_message.values())==True:
                return Response({
                    "success"   : False,
                    "error"     : err_message,
                    "message"   : "Please correct listed errors!!"
                    })

            email_data = EmailVerify.objects.filter(email=post_data['email'].lower(),\
                mphin=post_data['mpin'],active_status=1,\
                Company_id=post_data['Company'],types='Online')
            if email_data.count() > 0:
                return Response({
                            "status": True,
                            "message": "Verify Successfully!!",
                            })
            else:
                return Response({
                                    "status": False,
                                    "message": "The MPIN entered by you is incorrect. Please enter the correct MPIN and try again."
                                })
        except Exception as e:
            print(e)
            return Response(
                {
                    "success": False,
                    "message": "MPIN Verify api stucked into exception!!",
                }
            )
