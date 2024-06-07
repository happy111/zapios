import json
import math
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from _thread import start_new_thread
from datetime import datetime
from django.db.models import Q
from Orders.models import Order, OrderStatusType, OrderTracking
from Brands.models import Company
from discount.models import Coupon
from History.models import CouponUsed
from frontApi.serializer.customer_serializers import CustomerSignUpSerializer
from frontApi.order.send_mail import *
from rest_framework_tracking.mixins import LoggingMixin

# Serializer for api
from rest_framework import serializers
from google_speech import Speech
from Product.models import Product
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile, UserType
from ZapioApi.api_packages import *
from History.models import CouponUsed
from Configuration.models import PaymentDetails
from Outlet.models import OutletProfile
from Location.models import *
from zapio.settings import  Media_Path
from Customers.models import CustomerProfile
from django.template.loader import render_to_string
from .order_info import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
class CouponUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponUsed
        fields = "__all__"
def genrate_invoice_number(number):
    length = len(str(number))
    if length < 6:
        aa = 6 - length
        for a in range(aa):
            number = "0" + str(number)
    return str(number)
def order_registration_notification(orderID, oid):
    orderdata = Order.objects.filter(id=orderID).first()
    alldata = {}
    nodata = {}
    y = orderdata.address
    x = orderdata.customer
    if x != None:
        if "name" in x:
            alldata["customer"] = x["name"]
        else:
            alldata["customer"] = ""
        if "mobile" in x:
            alldata["mobile"] = x["mobile"]
        else:
            alldata["mobile"] = ""
        if "email" in x:
            alldata["email"] = x["email"]
        else:
            alldata["email"] = ""
        if "address" in x:
            alldata["address"] = x["address"]
        else:
            alldata["address"] = ""
    else:
        alldata["customer"] = ""
        alldata["mobile"] = ""
        alldata["email"] = ""
        alldata["address"] = ""
    alldata["company"] = orderdata.Company.id
    chkuser = CustomerProfile.objects.filter(
        Q(mobile=alldata["mobile"]), Q(company=alldata["company"])
    )
    if chkuser.count() > 0:
        a = {}
        cadr = chkuser[0].address1
        chka = y[0]["address"]
        loc = y[0]["locality"]
        for k in cadr:
            if k["address"] == chka and k["locality"] == loc:
                pass
            else:
                alls = {}
                nl = k["locality"]
                na = k["address"]
                alls["locality"] = nl
                alls["address"] = na
                alls["address_type"] = k["address_type"]
                cadr.append(alls)
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
            print("Error", customer_registration_serializer.errors)
    else:
        cust_data = {}
        cust_data["mobile"] = alldata["mobile"]
        cust_data["email"] = alldata["email"]
        cust_data["company"] = alldata["company"]
        cust_data["address"] = alldata["address"]
        cust_data["name"] = alldata["customer"]
        cust_data["address1"] = y
        cust_data["pass_pin"] = otp_generator()
        username = str(cust_data["company"]) + str(cust_data["mobile"])
        cust_data["username"] = username
        cust_data["active_status"] = 1
        cUser = User.objects.filter(username=username)
        if cUser.count() > 0:
            cU = User.objects.filter(username=username).first()
            cust_data["auth_user"] = cU.id
        else:
            create_user = User.objects.create_user(
                username=username,
                email=cust_data["email"],
                password=cust_data["pass_pin"],
                is_staff=False,
                is_active=True,
            )
            cust_data["auth_user"] = create_user.id
        customer_registration_serializer = CustomerSignUpSerializer(data=cust_data)
        if customer_registration_serializer.is_valid():
            customer_data_save = customer_registration_serializer.save()
            nodata["users"] = customer_data_save.id
            order_serializer = OrderSerializer(orderdata, data=nodata, partial=True)
            if order_serializer.is_valid():
                order_serializer.save()
            else:
                print(order_serializer.errors)
        else:
            print("error", customer_registration_serializer.errors)


def order_email_otp_notification(order, customer, key, secret):
    try:
        url = " https://api.razorpay.com/v1/invoices"
        data = {}
        data["type"] = "link"
        data["amount"] = int(order.total_bill_value) * 100
        data["view_less"] = 1
        data["currency"] = "INR"
        data["description"] = "Payment for order " + str(order.id)
        data["customer"] = {}
        data["customer"]["name"] = customer["name"]
        data["reminder_enable"] = True
        if customer["email"]:
            data["customer"]["email"] = customer["email"]
            data["email_notify"] = 1
        if customer["mobile"]:
            data["customer"]["contact"] = customer["mobile"]
            data["sms_notify"] = 1
        data = json.dumps(data)
        headers = {"Content-type": "application/json"}
        response = requests.post(url, data=data, headers=headers, auth=(key, secret),)
        print("done", response.content)
    except Exception as e:
        print(e)
        pass


def order_sms_notification(order_id, status):
    notification_instance = OrderSMSNotification(order_id=order_id, status=status)
    notification_instance()


class EditOrderProcess(LoggingMixin, APIView):
    """
    Customer Order Update POST API

        Authentication Required     : Yes
        Service Usage & Description : This Api is used to update all order related
        data to store it in database for future reference.

        Data Post:  {
            "order_id" : 1,
            "customer": {
                            "name": "umesh",
                            "mobile": "8423845784",
                            "email" : "umeshsamal3@gmail.com"
                        },

             "address1": [
                            {
                               "address_type"  : "Home"
                               "locality": "Ashram",
                                "address": "Hari Nagar Ashram",
                            },
                            {
                                "locality": "3.142542",
                                "address": "Mayur Vihar",
                            }
                        ],

            settlement_details:[
                        {"mode":"0","amount":250},
                        {"mode":"1","amount":150,"transaction_id":"razr_012365478uytre"}
                        ],

            "order_description": [
                                    {
                            "name": "Margreeta Pizza",
                            "id": "12",
                            "price": "229",
                            "size": "N/A",
                            "customization_details": []
                        
                            },
                            {
                            "name": "Margreeta Pizza",
                            "id": "12",
                            "price": "229",
                            "size": "N/A",
                            "customization_details": []
                        
                            }
                        ],
            
            "payment_mode": "1",
            "payment_id" : "Razor1539587456980",
            "Payment_status" : "1",
            "discount_value": 0,
            "total_bill_value": 309,
            "total_items": 2,
            "sub_total": 294,
            "cart_discount": 0,
            "discount_name": "",
            "discount_reason": "",
            "Delivery_Charge": 309,
            "Packing_Charge": 0,
            "Order_Type": "takeaway",
            "Payment_source":"paytm",
            "Order_Source" : "call",
            "delivery_instructions": "asdsadsa",
            "special_instructions": "dasdsadsa",
            "outlet_id" : 3,
            "taxes": 15,
            
        }

        Response: {

            "success": true,
            "message": "Order Updated successfully"
        }

    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data
            orderdata = {}
            user = request.user
            co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
            err_message = {}
            orderdata["Company"] = co_id
            err_message["Order_Type"] = validation_master_anything(
                data["Order_Type"], "Order Type", alpha_re, 3
            )
            sdetails = data["settlement_details"]
            if len(sdetails) > 0:
                for i in sdetails:
                    if "mode" in i and "amount" in i:
                        pass
                    else:
                        err_message[
                            "payment_detail"
                        ] = "Order mode and amount value is not set!!"
                        break
                    if i["mode"] != 0:
                        if "mode" in i and "amount" in i and "transaction_id" in i:
                            orderdata["transaction_id"] = i["transaction_id"]
                        else:
                            err_message[
                                "payment_detail"
                            ] = "Order mode and amount and trannsaction_id value is not set!!"
                            break
                    else:
                        pass
            else:
                pass
            try:
                data["taxes"] = float(data["taxes"])
            except Exception as e:
                err_message["tax"] = "Tax Price value is not valid!!"
            try:
                data["Delivery_Charge"] = float(data["Delivery_Charge"])
            except Exception as e:
                err_message["Delivery_Charge"] = "Delivery Price value is not valid!!"
            try:
                data["Packing_Charge"] = float(data["Packing_Charge"])
            except Exception as e:
                err_message["Packing_Charge"] = "Packing Price value is not valid!!"
            try:
                data["cart_discount"] = float(data["cart_discount"])
            except Exception as e:
                err_message["cart_discount"] = "Discount value is not valid!!"
            try:
                data["sub_total"] = float(data["sub_total"])
            except Exception as e:
                err_message["sub_total"] = "Sub total value is not valid!!"

            record = Order.objects.filter(id=data['order_id'])

            if record.count() > 0:
                pass
            else:
                err_message["order_id"] = "Provided Order data is not valid to retrieve!!"

            if any(err_message.values()) == True:
                return Response(
                    {
                        "success": False,
                        "error": err_message,
                        "message": "Please correct listed errors!!",
                    }
                )
            orderdata["order_description"] = data["order_description"]
            orderdata["customer"] = data["customer"]
            company_query = Company.objects.filter(id=co_id)
            last_id_q = Order.objects.filter(Company_id=co_id).last()
            if last_id_q:
                last_id = str(last_id_q.id)
            else:
                last_id = "001"
            sn = company_query[0].company_name
            out_id = data["outlet_id"]
            outlet_wise_order_count = Order.objects.filter(
                Q(Company_id=orderdata["Company"]), Q(outlet_id=data["outlet_id"])
            ).count()
            if outlet_wise_order_count > 0:
                final_outlet_wise_order_count = int(outlet_wise_order_count) + 1
            else:
                final_outlet_wise_order_count = 1
            a = genrate_invoice_number(final_outlet_wise_order_count)
            finalorderid = str(sn) + str(out_id) + "-" + str(2021) + str(a)
            orderdata["user"] = ManagerProfile.objects.filter(auth_user_id=user.id)[
                0
            ].username
            company_name = company_query[0].company_name
            orderdata["order_time"] = datetime.now()
            orderdata["taxes"] = data["taxes"]
            orderdata["delivery_instructions"] = data["delivery_instructions"]
            orderdata["special_instructions"] = data["special_instructions"]
            if len(data["settlement_details"]) > 0:
                Order_status_q = OrderStatusType.objects.filter(
                    Order_staus_name__icontains="Settle"
                )
            else:
                Order_status_q = OrderStatusType.objects.filter(
                    Order_staus_name__icontains="Received"
                )
            orderdata["order_status"] = Order_status_q[0].id
            orderdata["sub_total"] = data["sub_total"]
            orderdata["discount_value"] = data["cart_discount"]
            orderdata["total_bill_value"] = data["total_bill_value"]
            orderdata["outlet"] = data["outlet_id"]
            orderdata["settlement_details"] = data["settlement_details"]
            orderdata["payment_source"] = data["Payment_source"]
            orderdata["order_source"] = data["Order_Source"]
            orderdata["packing_charge"] = data["Packing_Charge"]
            orderdata["delivery_charge"] = data["Delivery_Charge"]
            orderdata["order_type"] = data["Order_Type"]
            orderdata["discount_name"] = data["discount_name"]
            orderdata["discount_reason"] = data["discount_reason"]
            orderdata["address"] = data["address1"]
            orderdata["customer"] = data["customer"]
            if "mobile" in data["customer"]:
                orderdata["mobile"] = data["customer"]["mobile"]
            else:
                orderdata["mobile"] = ""
            orderdata["tax_detail"] = data["tax_detail"]
            order_serializer = OrderSerializer(record[0],data=orderdata,partial=True)
            if order_serializer.is_valid():
                order_obj = order_serializer.save()
                orderid = order_serializer.data["id"]
                oid = order_serializer.data["order_id"]
                start_new_thread(order_registration_notification, (orderid, oid))
                payment_details = PaymentDetails.objects.filter(
                    company__id=co_id
                ).first()
                key = payment_details.keyid
                secret = payment_details.keySecret
                if key and secret:
                    order_email_otp_notification(
                        order_obj, data["customer"], key, secret
                    )
                ccode = Order.objects.filter(id=orderid).first().coupon_code
                if ccode == "" or ccode == None:
                    pass
                else:
                    code_check = Coupon.objects.filter(
                        coupon_code__exact=ccode, active_status=1
                    )
                    if code_check.count() != 0:
                        frequency = code_check[0].frequency
                        updated_freq = frequency - 1
                        code_update_q = code_check.update(frequency=updated_freq)
                    else:
                        pass
                    used_coupon = {}
                    used_coupon["Coupon"] = code_check[0].id
                    used_coupon["customer"] = orderdata["customer"]
                    used_coupon["order_id"] = orderid
                    used_coupon["Company"] = data["company_id"]
                    used_coupon["created_at"] = datetime.now()
                    usedcoupon_serializer = CouponUsedSerializer(data=used_coupon)
                    if usedcoupon_serializer.is_valid():
                        usedcoupon_serializer.save()
                    else:
                        print(str(order_serializer.errors))
                        return Response(
                            {
                                "success": False,
                                "message": str(usedcoupon_serializer.errors),
                            }
                        )
                print("SMS Passed.")
                data['orderid'] = record[0].outlet_order_id
                data_info = OrderInfo(orderid)
                return Response(
                    {"success": True, 
                      "data"  : data_info,
                     "message": "Order Updated successfully"}
                )
            else:
                print(str(order_serializer.errors))
                return Response(
                    {"success": False, "message": str(order_serializer.errors)}
                )
        except Exception as e:
            print(e)
            return Response(
                {
                    "success": False,
                    "message": "Order place api stucked into exception!!",
                }
            )
