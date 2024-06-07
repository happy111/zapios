import math,json
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
from rest_framework_tracking.mixins import LoggingMixin

# Serializer for api
from rest_framework import serializers
from google_speech import Speech
from .send_mail import *
from .verify import *
from Product.models import Product
from Location.models import *
from ZapioApi.api_packages import *
from Configuration.models import PaymentMethod,OrderSource




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CouponUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponUsed
        fields = "__all__"


def order_sms_notification(order_id, status):
    notification_instance = OrderSMSNotification(order_id=order_id, status=status)
    notification_instance()


class OrderData(LoggingMixin, APIView):
    """
    Customer Order POST API

        Authentication Required     : No
        Service Usage & Description : This Api is used to save all order related
        data to store it in database for future reference.

        #  Note : Donot Miss key
        Data Post:  {
                        {
                        "customer": {
                                    "name": "Sanoth", (c)                                       
                                    "mobile_number": "9543456757",(c)
                                    "email": "umesh@eoraa.com", (c)
                                    },
                        "address": [
                            {
                               "address_type"  : "Home" (c)
                               "locality": "1", 
                               "address": "Hari Nagar Ashram", (c)
                               "longitude": "3.142542", (c)
                               "latitude" : "3.236542",  (c)
                               "pincode"  :  110014      (c)
                               "city"     : "1",
                               "country"  : "India"
                             },

                        ],
                        "order_time": "2020-08-31 04:25:00.000000",
                        "company_id" : "1",
                        "delivery_instructions": "",
                        "Company_outlet_details" : {},
                        "order_description": [
                                                {
                                        "name": "Margreeta Pizza",
                                        "id": "533",
                                        "price": "229",
                                        "size": "N/A",
                                        "quantity" : "1",
                                        "customization_details": []
                                        },
                                        {
                                        "name": "Cold Drink",
                                        "id": "533",
                                        "price": "65",
                                        "size": "N/A",
                                        "quantity" : "1",
                                        "customization_details": []
                                        }
                                    ],
                        "taxes": 100,
                        "payment_mode": "1",
                        "payment_id" : "Razor1539587456980",
                        "Payment_status" : "1",
                        "special_instructions": "",
                        "sub_total": 294,
                        "discount_value": 0,
                        "total_bill_value": 309,
                        "total_items": 2,
                        "coupon_code" : "",
                        "shop_id" : 34,
                        "order_source": 4,   (13 for website)
                        "delivery_charge":"50",
                        "packing_charge" : "10",
                        "is_order_now"   : '1'   1=order Now  0=Order latter
                        "schedule_delivery_time" : "2020-08-31 04:25:00.000000",
                        "tax_detail"  :
                                      [
                                         {
                                            "id": "9",
                                            "tax_amount"  : "50"
                                          },
                                     ]
                     }
            }

        Response: {

            "success": true,
            "message": "Order Received successfully"
        }

    """

    def post(self, request, format=None):
        try:
            post_data = request.data
            orderdata = {}
            err_message = {}
            orderdata["order_description"] = post_data["order_description"]
            pdata = orderdata["order_description"]
            dataorder = len(pdata)
            pro_id = pdata[0]["product_id"]
            cid = Product.objects.filter(id=pro_id).first().Company_id
            orderdata["Company_outlet_details"] = post_data["Company_outlet_details"]
            orderdata["address"] = post_data["address"]
            orderdata["customer"] = post_data["customer"]
            company_query = Company.objects.filter(id=cid)
            chk_payment = PaymentMethod.objects.filter(company_id=cid,id=post_data['payment_mode'])
            if chk_payment.count() > 0:
                pass
            else:
                err_message['payment_mode'] = "Payment mode data is not valid!!"
            err_message["order_source"] = \
                    only_required(post_data["order_source"],"Order Source")
            chk_source = OrderSource.objects.filter(id = post_data['order_source'],company_id=cid)
            if chk_source.count() > 0:
                pass
            else:
                err_message["order_source"] = "Order Source data is not valid!!"
            if post_data['is_order_now'] == 0:
                if post_data['schedule_delivery_time'] == '':
                    err_message["schedule_delivery_time"] = "Please Enter schedule_delivery_time!!"
            else:
                pass
            if post_data["order_type"] == 'Takeaway':
                pass
            else:
                err_message["address_type"] = \
                        only_required(post_data["address"][0]['address_type'],"Address type")
            tax_detail = post_data['tax_detail']
            if type(post_data['tax_detail']) == list:
                tax_detail = post_data['tax_detail']
                if len(post_data['tax_detail']) > 0:
                    for i in tax_detail:
                        if "id" in i and "tax_amount" in i:
                            pass
                        else:
                            err_message[
                                "tax_detail"
                            ] = " 'id' or  'tax_amount' value is not set!!"
                            break
            else:
                err_message["tax_detail"] = "Please send data array format!!"
            if any(err_message.values())==True:
                return Response({
                    "success"   : False,
                    "error"     : err_message,
                    "message"   : "Please correct listed errors!!"
                    })
            last_id_q = Order.objects.filter(Company_id=cid).last()
            if last_id_q:
                last_id = str(last_id_q.id)
            else:
                last_id = "001"
            last_oid_q = Order.objects.filter(outlet_id=post_data["shop_id"])
            if last_oid_q.count() > 0:
                last_oid_q = Order.objects.filter(outlet_id=post_data["shop_id"]).last()
            else:
                last_oid_q = 0
            sn = company_query[0].company_name
            out_id = post_data["shop_id"]
            outlet_wise_order_count = Order.objects.filter(
                Q(Company_id=cid), Q(outlet_id=post_data["shop_id"])
            )
            if outlet_wise_order_count.count() > 0:
                final_outlet_wise_order_count = int(outlet_wise_order_count.count()) + 1
            else:
                final_outlet_wise_order_count = 1
            a = genrate_invoice_number(final_outlet_wise_order_count)
            finalorderid = str(sn) + str(out_id) + "-" + str(2021) + str(a)
            company_name = company_query[0].company_name
            orderdata["order_id"] = company_name + last_id
            orderdata["outlet_order_id"] = finalorderid
            orderdata["order_description"] = post_data["order_description"]
            orderdata["taxes"] = post_data["taxes"]
            orderdata["delivery_instructions"] = post_data["delivery_instructions"]
            orderdata["special_instructions"] = post_data["special_instructions"]
            # orderdata["note"] = post_data["note"]

            orderdata["payment_mode"] = chk_payment[0].payment.payment_method
            Order_status_q = OrderStatusType.objects.filter(
                Order_staus_name__icontains="Received"
            )
            orderdata["order_status"] = Order_status_q[0].id
            orderdata["sub_total"] = post_data["sub_total"]
            orderdata["discount_value"] = post_data["discount_value"]
            orderdata["transaction_id"] = post_data["payment_id"]
            orderdata["coupon_code"] = post_data["coupon_code"]
            orderdata["is_paid"] = post_data["Payment_status"]
            orderdata["total_bill_value"] = post_data["total_bill_value"]
            orderdata["total_items"] = post_data["total_items"]
            orderdata["outlet"] = post_data["shop_id"]
            orderdata["order_source"] = post_data["order_source"]
            orderdata["delivery_charge"] = post_data["delivery_charge"]
            orderdata["packing_charge"] = post_data["packing_charge"]
            orderdata["Company"] = cid
            orderdata["mobile"] = post_data["customer"]["mobile_number"]
            orderdata["is_order_now"] = post_data["is_order_now"]
            orderdata["tax_detail"] = post_data["tax_detail"]
            orderdata["order_type"] = post_data["order_type"]

            now = datetime.now()
            orderdata["day"] = now.strftime("%A")
            if post_data['is_order_now'] == 0:
                orderdata["schedule_delivery_time"] = post_data["schedule_delivery_time"]['date']
                orderdata["schedule_time"] = post_data["schedule_delivery_time"]['time']
                orderdata["order_time"] = post_data["schedule_delivery_time"]['date']
            else:
                orderdata["order_time"] = post_data["order_time"]
            orderdata["user"] = Company.objects.filter(id=cid)[0].username
            order_record = Order.objects.filter(Company=orderdata["Company"])
            if order_record.count() != 0:
                is_visited = order_record.filter(
                    customer__mobile_number=post_data["customer"]["mobile_number"]
                )
                if is_visited.count() == 0:
                    pass
                else:
                    orderdata["has_been_here"] = 1
                    is_visited.update(has_been_here=1)
            else:
                pass

            # data_verify = DataVerify(post_data)
            # min_data_verify = data_verify - 1
            # max_data_verify = data_verify + 1
            # if orderdata["coupon_code"] == "" or orderdata["coupon_code"] == None or orderdata["coupon_code"] == str(0):
            #     pass
            # else:
            #     orderdata['total_bill_value'] = orderdata['total_bill_value'] - float(post_data['order_description'][0]['discount'])
            
            # if min_data_verify <=  orderdata["total_bill_value"] or max_data_verify >= orderdata['total_bill_value']:
            #     return Response({
            #         "success"   : False,
            #         "error"     : err_message,
            #         "message"   : "Sorry Order is not placed!! because price not match our database"
            #         })
            # else:
            #     return Response({
            #         "success"   : False,
            #         "error"     : err_message,
            #         "message"   : "Sorry Order is not placed!! because price not match our database"
            #         })
            order_serializer = OrderSerializer(data=orderdata)
            if order_serializer.is_valid():
                order_serializer.save()
                orderid = order_serializer.data["id"]
                oid = order_serializer.data["outlet_order_id"]
                start_new_thread(order_email_notification, (orderid, oid, post_data))
                start_new_thread(
                    order_registration_notification, (orderid, oid, post_data)
                )
                order_id = order_serializer.data["order_id"]
                status = Order_status_q[0].Order_staus_name
                # start_new_thread(order_sms_notification, (order_id, status))
                ccode = Order.objects.filter(id=orderid).first().coupon_code
                if ccode == "" or ccode == None or ccode == str(0):
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
                    used_coupon["Company"] = orderdata["Company"]
                    used_coupon["outlet"] = orderdata["outlet"]
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
                order_tracking = OrderTracking.objects.create(
                    order_id=orderid,
                    Order_staus_name_id=orderdata["order_status"],
                    created_at=datetime.now(),
                )
                #start_new_thread(order_confirmation, (orderid,cid))
                return Response(
                    {
                     "success": True, 
                     "order_id" : oid,
                     "message": "Order Received successfully"}
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



