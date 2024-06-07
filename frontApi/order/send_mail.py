import requests
import json
import geopy.distance
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from zapio.settings import (
    Media_Path,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    SMS_FROM,
    MSG91_AUTHKEY,
    MSG91_Notification_FLOWID,
    MSG91_URL,
)
from Outlet.models import OutletProfile
from Brands.models import Company
from Orders.models import Order, OrderStatusType, OrderTracking
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from _thread import start_new_thread
from Customers.models import CustomerProfile
from django.db.models import Q
from frontApi.serializer.customer_serializers import CustomerSignUpSerializer
from Configuration.models import ColorSetting, EmailSetting
from datetime import datetime
from googlegeocoder import GoogleGeocoder
from googlemaps import Client
from twilio.rest import Client as twilio_client
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from rest_framework import serializers
from Customers.serializers.notification_serializers import (
    NotificationRecordSerializer,
)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


def email_send_module(toe, oid, send_data, company_id,cd):
    try:
        order_mail = Company.objects.filter(id=company_id)[0].support_person_email_id
      
        c = Company.objects.filter(id=company_id)
        cname = c[0].company_name
        mail_subject = "Your Order " + oid + " has been accepted."
        to = toe
        cc_email_id = []
        to_email = [
            to,
        ]
        track_url = c[0].website+'/order?_order_tracker_=' + str(send_data['id']) 
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {'Content-type': 'application/json',
            "Authorization": "Bearer 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",
           'Accept': 'application/json'}
        data = {
              "personalizations": [
                {
                  "to": [
                    {
                      "email": toe,
                    },
                  ],
                  "dynamic_template_data": {
                  "items1":cd,
                  "outletname":send_data['outletname'],
                  "order" : send_data['orderid'],
                  "order_date" : send_data['order_time'],
                  "track_url"  : track_url,
                  "accepted_time" : datetime.now().strftime("%I:%M %p"),
                    'tax': send_data['tax'],
                    'patmentmode': send_data['patmentmode'],
                    'payment_id': send_data['payment_id'], 
                    'sub_total': round(send_data['sub_total'],2),
                    'discount_value': round(send_data['discount_value'],2) ,
                    'total_bill_value': round(send_data['total_bill_value'],2),
                    'total_items': send_data['total_items'], 
                    'address1': send_data['address1'],
                    'locality': send_data['locality'], 
                    'customer': send_data['customer'],
                    'mobile_number': send_data['mobile_number'], 
                    'emails': send_data['emails'], 
                    'orderid': send_data['orderid'],
                    'outletname': send_data['outletname'], 
                    'address': send_data['address'], 
                    'city': send_data['city'], 
                    'company_name': send_data['company_name'], 
                    'order_time': send_data['order_time'], 
                    'delivery_charge': round(send_data['delivery_charge'], 2),
                    'packing_charge': round(send_data['packing_charge'],2),
                    "support_email" :  order_mail 
 
                  },

                }
              ],
              "from": {
                "email": "umeshsamal070@gmail.com",
                "name" : cname
              },
                "subject": mail_subject,
                "template_id":"d-e3da8f9ee26747689da6ea26a098e132",
                "content": [{"type": "text/html", "value": "Heya!"}]
            }
        print(data)
        response= requests.post(url,data=json.dumps(data),headers=headers)
        print(response)
        return response
    except Exception as e:
        print(e)


def email_user_send_module(toe, send_data):
    try:
        subject = "Registration Detail"
        from_email = EMAIL_HOST_USER
        to = toe
        cc_email_id = []
        to_email = [
            to,
        ]
        html_content = render_to_string(
            "email_templates/user-emailer.html", {"data1": send_data}
        )
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, to_email, cc=cc_email_id
        )
        msg.attach_alternative(html_content, "text/html")
        result_of_mail = msg.send()
        return result_of_mail
    except Exception as e:
        print(e)


def order_email_notification(orderID, oid, datas):
    import datetime
    from discount.models import PercentOffers
    orderdata = Order.objects.filter(id=orderID).first()
    company_id = orderdata.Company_id
    today = datetime.datetime.now()
    cname = Company.objects.filter(id=company_id)[0]
    emaildata = EmailSetting.objects.filter(company_id=company_id)
    themedata = ColorSetting.objects.filter(company_id=company_id)
    alldata = {}
    alldata["order_time"] = orderdata.order_time
    alldata["taxes"] = str(orderdata.taxes)[:4]
    alldata["payment_mode"] = orderdata.payment_mode
    if alldata["payment_mode"] == "0":
        alldata["trans_id"] = "N/A"
    else:
        alldata["trans_id"] = orderdata.payment_id
    alldata["payment_id"] = orderdata.transaction_id
    alldata["sub_total"] = orderdata.sub_total
    alldata["discount_value"] = orderdata.discount_value
    alldata["total_bill_value"] = orderdata.total_bill_value
    alldata["total_items"] = orderdata.total_items
    alldata["company"] = orderdata.Company.company_logo
    alldata["website"] = orderdata.Company.website
    alldata["shop_id"] = orderdata.outlet_id
    alldata["final"] = Media_Path + str(alldata["company"])
    outletdetails = OutletProfile.objects.filter(id=int(alldata["shop_id"])).first()
    addressdata = orderdata.address
    addressdata = orderdata.customer
    alldata["customer"] = addressdata["name"]
    alldata["mobile_number"] = addressdata["mobile_number"]
    alldata["email"] = addressdata["email"]
    cd = orderdata.order_description
    c = []
    for i in range(len(cd)):
        orderdes = {}
        orderdes["name"] = cd[i]["name"]
        orderdes["price"] = cd[i]["price"]
        c.append(orderdes)
    send_data = {
        "tax": alldata["taxes"],
        "patmentmode": alldata["payment_mode"],
        "payment_id": alldata["payment_id"],
        "sub_total": alldata["sub_total"],
        "discount_value": alldata["discount_value"],
        "total_bill_value": alldata["total_bill_value"],
        "total_items": alldata["total_items"],
        "logo": alldata["final"],
        "address1": orderdata.address[0]["address"],
        "locality": orderdata.address[0]["locality"],
        "customer": alldata["customer"],
        "mobile_number": alldata["mobile_number"],
        "emails": alldata["email"],
        "orderid": oid,
        "outletname": outletdetails.Outletname,
        "address": outletdetails.address,
        "city": outletdetails.city,
        "order_cart_list": cd,
        "trans_id": alldata["trans_id"],
        "accent_color": themedata[0].accent_color,
        "textColor": themedata[0].textColor,
        "secondaryColor": themedata[0].secondaryColor,
        "company_name": cname.company_name,
        "address": cname.address,
        "order_time": alldata["order_time"].strftime("%d %B %Y %I:%M %p"),
        "delivery_charge": orderdata.delivery_charge,
        "packing_charge": orderdata.packing_charge,
        "id" : orderID
    }
    datas["company_name"] = cname.company_name
    datas["product_desc"] = cd
    datas["logo"] = alldata["final"]
    datas["outlet_name"] = outletdetails.Outletname
    datas["order_id"] = oid
    to_emailID_list = alldata["email"]
    email_send_status = email_send_module(to_emailID_list, oid, send_data, company_id,cd)


def order_registration_notification(orderID, oid, postdata):
    orderdata = Order.objects.filter(id=orderID).first()
    alldata = {}
    nodata = {}
    sdata = {}
    alldata["company"] = orderdata.Company.company_logo
    alldata["final"] = Media_Path + "/media/" + str(alldata["company"])
    alldata["shop_id"] = orderdata.outlet_id
    alldata["final"] = Media_Path + str(alldata["company"])
    outletdetails = OutletProfile.objects.filter(id=int(alldata["shop_id"])).first()
    address_data = postdata["address"]
    for index in address_data:
        if "type" in index:
            alldata["address_type"] = index["address_type"]
        else:
            pass
        if "address" in index:
            alldata["address"] = index["address"]
        else:
            pass
        if "latitude" in index:
            alldata["latitude"] = index["latitude"]
        else:
            alldata["latitude"] = ""
        if "longitude" in index:
            alldata["longitude"] = index["longitude"]
        else:
            alldata["longitude"] = ""
        if "locality" in index:
            alldata["locality"] = index["locality"]
        else:
            alldata["locality"] = ""
        if "pincode" in index:
            alldata["pincode"] = index["pincode"]
        else:
            alldata["pincode"] = ""
    # Distance Calculate
    if (
        alldata["latitude"] != None
        and alldata["longitude"] != None
        and alldata["latitude"] != ""
        and alldata["longitude"] != ""
    ):
        customer_location = (alldata["latitude"], alldata["longitude"])
        outlet_location = (outletdetails.latitude, outletdetails.longitude)
        unloaded_mile = great_circle(outlet_location, customer_location).miles
        kilometers = round((unloaded_mile // 0.62137119), 2)
        sdata["distance"] = kilometers
        order_serializer = OrderSerializer(orderdata, data=sdata, partial=True)
        if order_serializer.is_valid():
            order_serializer.save()
        else:
            pass
    else:
        pass
    od_data = orderdata.customer
    alldata["customer"]          = od_data["name"]
    alldata["mobile_number"]     = od_data["mobile_number"]
    alldata["email"]             = od_data["email"]
    alldata["company"]           = orderdata.Company.id

    chkuser = CustomerProfile.objects.filter(
        Q(email=alldata['email']),\
        Q(company=alldata["company"])
    )
    

    if chkuser.count() > 0:
        a = {}
        cadr    = chkuser[0].address1
        chka    = address_data[0]["address"]
        loc     = address_data[0]["locality"]
        result = []
        flag = 1
        if cadr != None and len(cadr) > 0:
            for k in cadr:
                if k["address"] == chka:
                    flag = 0
                else:
                    pass
        if flag == 1:
            if cadr != None and len(cadr) > 0:
                pass
            else:
                cadr = []
            alls = {}
            alls["locality"] = loc
            alls["address"] = chka
            if 'city' in address_data[0]:
                alls["city"] = address_data[0]["city"]
            else:
                pass
            if 'state' in address_data[0]:
                alls["state"] = address_data[0]["state"]
            else:
                pass
            if 'pincode' in address_data[0]:
                alls["pincode"] = address_data[0]["pincode"]
            else:
                pass
            if 'address_type' in address_data[0]:
                alls["address_type"] = address_data[0]["address_type"]
            else:
                pass
            if 'longitude' in address_data[0]:
                alls["longitude"] = address_data[0]["longitude"]
            if 'latitude' in address_data[0]:
                alls["latitude"] = address_data[0]["latitude"]
            cadr.append(alls)
        else:
            pass
        a["address1"] = cadr
        customer_registration_serializer = CustomerSignUpSerializer(
            chkuser[0], data=a, partial=True
        )
        if customer_registration_serializer.is_valid():
            customer_data_save = customer_registration_serializer.save()
            nodata["users"] = customer_data_save.id
            order_serializer = OrderSerializer(orderdata, data=nodata, partial=True)
            if order_serializer.is_valid():
                order_serializer.save()
            else:
                print(order_serializer.errors)
        else:
            pass
    else:
        cust_data = {}
        cust_data["mobile"] = alldata["mobile_number"]
        cust_data["email"] = alldata["email"]
        cust_data["company"] = alldata["company"]
        cust_data["address1"] = postdata["address"]
        cust_data["latitude"] = alldata["latitude"]
        cust_data["longitude"] = alldata["longitude"]
        cust_data["name"] = postdata["customer"]["name"]
        cust_data["pass_pin"] = otp_generator()
        username = str(cust_data["company"]) + str(cust_data["mobile"])
        cust_data["username"] = username
        cust_data["active_status"] = 1
        # cUser = User.objects.filter(username=username)
        # if cUser.count() > 0:
        #     cU = User.objects.filter(username=username).first()
        #     cust_data["auth_user"] = cU.id
        # else:
        #     create_user = User.objects.create_user(
        #         username=username,
        #         email=cust_data["email"],
        #         password=cust_data["pass_pin"],
        #         is_staff=False,
        #         is_active=True,
        #     )
        #     cust_data["auth_user"] = create_user.id
        customer_registration_serializer = CustomerSignUpSerializer(data=cust_data)
        if customer_registration_serializer.is_valid():
            customer_data_save = customer_registration_serializer.save()
            nodata["users"] = customer_data_save.id
            order_serializer = OrderSerializer(orderdata, data=nodata, partial=True)
            if order_serializer.is_valid():
                order_serializer.save()
            else:
                print(order_serializer.errors)
            send_data = {
                "logo": alldata["final"],
                "address1": postdata["address"],
                "locality": alldata["locality"],
                "customer": alldata["customer"],
                "mobile_number": alldata["mobile_number"],
                "emails": alldata["email"],
                "outletname": outletdetails.Outletname,
                "username": cust_data["mobile"],
                "address": outletdetails.address,
                "city": outletdetails.city,
                "mobile": cust_data["mobile"],
                "email": cust_data["email"],
                "password": cust_data["pass_pin"],
                "name": cust_data["name"],
            }
            to_emailID_list = cust_data["email"]
        else:
            pass
    return "Success"



def otp_generator():
    import random
    otp = random.randint(1000, 9999)
    return otp


class OrderSMSNotification:
    def __init__(self, **notification_data):
        self.name = None
        self.status = None
        self.order_status = notification_data.get("status", None)
        self.customer_details = None
        self.order_id = notification_data.get("order_id", None)
        self.message_body = (
            "Hi ##name##, Your order with order ID: ##order_id## has been ##status##."
        )
        self.current_datetime = datetime.now().strftime("%d %B %Y %I:%M %p")
        self.mobileNumber = ""
        self.mobileNumberwoISD = ""
        self.country_customer = ""
        self.company_id = None
        self.reason_for_failed = None

    def sms_send_module(self):
        try:
            self.message_body = (
                str(self.message_body)
                .replace("##name##", str(self.name))
                .replace("##order_id##", str(self.order_id))
                .replace("##status##", str(self.order_status))
            )
            if self.country_customer == "IND":
                headers = {"authkey": MSG91_AUTHKEY, "Content-Type": "application/json"}
                data = {
                    "flow_id": MSG91_Notification_FLOWID,
                    "sender": "AIZOTC",
                    "recipients": [
                        {
                            "mobiles": self.mobileNumber,
                            "names": self.name,
                            "order_id": self.order_id,
                            "status": self.order_status,
                            
                        }
                    ],
                }
                data = json.dumps(data)
                resp = requests.post(url=MSG91_URL, data=data, headers=headers)
                resp_data = json.loads(resp.text)
                if resp_data["type"] == "success":
                    self.status = True
                if self.status == False:
                    self.reason_for_failed = resp_data["message"]
            else:
                client = twilio_client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                text = self.message_body
                to = self.mobileNumber
                payload = client.messages.create(from_=SMS_FROM, body=text, to=to)
                if payload.error_message == None:
                    self.status = True
                if self.status == False:
                    self.reason_for_failed = payload.error_message
                print(payload.body)
                print(payload.error_message)
                print(payload.status)
        except Exception as e:
            print(str(e))

    def notification_record_saved(self):
        customer_profile = CustomerProfile.objects.filter(
            Q(mobile=self.mobileNumberwoISD), Q(company__id=self.company_id),
        )
        self.customer_id = None
        if customer_profile.count():
            self.customer_id = customer_profile[0].id
        notification_record = {
            "notification_category": "SMS",
            "notification_type": None,
            "user": self.customer_id,
            "admin_user": None,
            "notification_for": "Customer",
            "reason_for_failed": self.reason_for_failed,
            "status": True,
            "message_data": None,
            "massge_body": self.message_body,
            "otp": None,
            "motp": None,
        }
        notification_record_serializer = NotificationRecordSerializer(
            data=notification_record
        )
        if notification_record_serializer.is_valid():
            notification_record_serializer.save()
        else:
            print("@@ notification_record_serializer-Errors @@")
            print(notification_record_serializer.errors)

    def get_customer_details(self):
        order_instance = Order.objects.filter(order_id=self.order_id).first()
        self.customer_details = order_instance.customer
        if self.customer_details:
            self.name = self.customer_details["name"]
            self.mobileNumber = (
                str(order_instance.Company.country.isd) + order_instance.mobile
            )
            self.country_customer = order_instance.Company.country.iso
            self.company_id = order_instance.Company.id
        if len(order_instance.mobile) > 0:
            self.mobileNumberwoISD = order_instance.mobile
            return True
        else:
            return False

    def main(self):
        resp = self.get_customer_details()
        if resp:
            self.sms_send_module()
            self.notification_record_saved()

    def __call__(self):
        self.main()


