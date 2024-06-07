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
from Outlet.models import OutletProfile
from Location.models import *
from zapio.settings import  Media_Path
from Customers.models import CustomerProfile
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from Configuration.models import *



def OrderInfo(id):
    order_record = Order.objects.filter(id=id)
    final_result = []
    p_list = {}
    p_list["id"]       = order_record[0].id
    p_list['order_id'] = order_record[0].order_id
    p_list["address"] = []
    if len(order_record[0].address) > 0:
        for index in order_record[0].address:
            dic = {}
            # if 'city' in index:
            #     try:
            #         city = int(index["city"])
            #         city_data = CityMaster.objects.filter(id=index['city'])
            #         if city_data.count() > 0:
            #             dic['city'] = city_data[0].city
            #         else:
            #             dic['cuty'] = index['city']
            #     except Exception as e:
            #         dic['cuty'] = index['city']
            # if 'locality' in index:
            #     try:
            #         locality = int(index["locality"])
            #         city_data = CityMaster.objects.filter(id=index['city'])
            #         locality_data = AreaMaster.objects.filter(id=index['locality'])
            #         if locality_data.count() > 0:
            #             dic['locality'] = locality_data[0].area
            #         else:
            #             dic['locality'] = index['locality']
            #     except Exception as e:
            #         dic['locality'] = index['locality']
            if 'address' in index:
                dic['address'] = index['address']
            else:
                dic['address'] = ''
            if 'address_type' in index:
                dic['address_type'] = index['address_type']
            else:
                dic['address_type'] = ''
            p_list['address'].append(dic)
    else:
        pass
    cus = order_record[0].customer
    if cus != "":
        p_list["name"] = cus["first_name"]
        if "email" in cus:
            p_list["email"] = cus["email"]
        else:
            pass
        if "mobile_number" in cus:
            p_list["mobile"] = cus["mobile_number"]
        if "mobile" in cus:
            p_list["mobile"] = cus["mobile"]
    else:
        pass
    p_list["order_description"] = order_record[0].order_description
    if order_record[0].order_time != None:
        o_time = order_record[0].order_time + timedelta(hours=5, minutes=30)
        p_list["order_time"] = o_time.strftime("%d/%b/%y %I:%M %p")
    else:
        pass
    p_list["log"] = []
    orderlog = OrderTracking.objects.filter(order_id=p_list["id"]).order_by("id")
    if orderlog.count() > 0:
        for j in orderlog:
            r_list = {}
            r_list["id"] = j.id
            r_list["status_name"] = j.Order_staus_name.Order_staus_name
            created_at = j.created_at + timedelta(hours=5, minutes=30)
            r_list["created_at"] = created_at.strftime("%d/%b/%y %I:%M %p")
            r_list["key_person"] = j.key_person
            p_list["log"].append(r_list)
    else:
        pass
    if order_record[0].delivery_time != None:
        d_time = order_record[0].delivery_time + timedelta(hours=5, minutes=30)
        p_list["delivery_time"] = d_time.strftime("%d/%b/%y %I:%M %p")
    else:
        p_list["delivery_time"] = None
    p_list["taxes"] = order_record[0].taxes
    p_list["sub_total"] = order_record[0].sub_total
    p_list["discount_value"] = order_record[0].discount_value
    p_list["total_bill_value"] = order_record[0].total_bill_value
    p_list["special_instructions"] = order_record[0].special_instructions
    p_list["is_rider_assign"] = order_record[0].is_rider_assign
    p_list["other_order_id"] = order_record[0].outlet_order_id
    p_list["cancel_reason"] = order_record[0].order_cancel_reason
    p_list["discount_name"] = order_record[0].discount_name
    p_list["cancel_responsibility"] = order_record[0].cancel_responsibility
    p_list["delivery_charge"] = order_record[0].delivery_charge
    p_list["packing_charge"] = order_record[0].packing_charge
    p_list["coupon_code"] = order_record[0].coupon_code
    p_list["order_source"] = order_record[0].order_source.source_name
    p_list["rider_detail"] = []
    if order_record[0].is_rider_assign == True:
        if order_record[0].is_aggregator == False:
            a = {}
            ad = DeliveryBoy.objects.filter(id=order_record[0].delivery_boy_id)
            a["name"] = ad[0].name
            a["email"] = ad[0].email
            a["mobile"] = ad[0].mobile
            p_list["rider_detail"].append(a)
        else:
            rider_detail = order_record[0].delivery_boy_details
            p_list["rider_detail"].append(rider_detail)
    else:
        a = {}
        a["name"] = ""
        a["email"] = ""
        a["mobile"] = ""
        p_list["rider_detail"].append(a)
    p_list["delivery_type"]   = order_record[0].delivery_type
    p_list["discount_reason"] = order_record[0].discount_reason
    p_list["distance"]     = order_record[0].distance
    p_list["mobile"]       = order_record[0].mobile
    p_list["delivery_instructions"] = order_record[0].delivery_instructions
    final_result.append(p_list)
    return final_result

    

def phone_check(data):
    err_message = {}
    orderdata = {}
    if 'address1' in data:
        # if 'city' in data['address1'][0]:
        #     try:
        #         data["City"] = int(data["address1"][0]['city'])
        #     except Exception as e:
        #         err_message["city"] = "City data is not valid!!"
        # else:
        #     err_message['city'] = "Please send 'city' key"
        # if 'locality' in data['address1'][0]:
        #     try:
        #         data["locality"] = int(data["address1"][0]['locality'])
        #     except Exception as e:
        #         err_message["locality"] = "Locality data is not valid!!"
        # else:
        #     err_message['city'] = "Please send 'locality' key"
        if 'address_type' in data['address1'][0]:
            pass
        else:
            err_message['address_type'] = "Please send 'address_type' key"
    else:
        err_message['address'] = "Please send 'address1' key"
    if 'customer' in data:
        pass
    else:
        err_message['customer'] = "Please send 'customer' key"
    if 'settlement_details' in data:
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
    else:
        err_message['settlement_details'] = "Please send 'settlement_details' key"

    if 'tax_detail' in data:
        if type(data['tax_detail']) == list:
            tax_detail = data['tax_detail']
            if len(data['tax_detail']) > 0:
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
    else:
         err_message["tax_detail"] = "Please send 'tax_detail' key"

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
    err_message["Order_Type"] = validation_master_anything(
                data["Order_Type"], "Order Type", alpha_re, 3)
    if any(err_message.values())==True:
        err = {
            "success": False,
            "error" : err_message,
            "message" : "Please correct listed errors!!"
            }
        return err
    else:
        return None




def zomato_check(data):
    err_message = {}
    orderdata = {}
    if 'address1' in data:
        
        # if 'city' in data['address1'][0]:
        #     try:
        #         data["City"] = int(data["address1"][0]['city'])
        #     except Exception as e:
        #         err_message["city"] = "City data is not valid!!"
        # else:
        #     err_message['city'] = "Please send 'city' key"
        
        # if 'locality' in data['address1'][0]:
        #     try:
        #         data["locality"] = int(data["address1"][0]['locality'])
        #     except Exception as e:
        #         err_message["locality"] = "Locality data is not valid!!"
        # else:
        #     err_message['city'] = "Please send 'locality' key"
        
        if 'address_type' in data['address1'][0]:
            pass
        else:
            err_message['address_type'] = "Please send 'address_type' key"
    else:
        err_message['address'] = "Please send 'address1' key"
    if 'customer' in data:
        if 'order_id' in data['customer']:
            err_message["order_id"] = \
            only_required(data["customer"]['order_id'],"Order ID")
        else:
            err_message['order_id'] = "Please send 'order_id' key"
    else:
        err_message['customer'] = "Please send 'customer' key"
    if 'settlement_details' in data:
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
    else:
        err_message['settlement_details'] = "Please send 'settlement_details' key"

    if 'tax_detail' in data:
        if type(data['tax_detail']) == list:
            tax_detail = data['tax_detail']
            if len(data['tax_detail']) > 0:
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
    else:
         err_message["tax_detail"] = "Please send 'tax_detail' key"

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
    err_message["Order_Type"] = validation_master_anything(
                data["Order_Type"], "Order Type", alpha_re, 3)
    if any(err_message.values())==True:
        err = {
            "success": False,
            "error" : err_message,
            "message" : "Please correct listed errors!!"
            }
        return err
    else:
        return None



def swiggy_check(data):
    err_message = {}
    orderdata = {}
    if 'address1' in data:
        pass
    else:
        err_message['address'] = "Please send 'address1' key"
    if 'customer' in data:
        if 'order_id' in data['customer']:
            err_message["order_id"] = \
            only_required(data['customer']["order_id"],"Order ID")
        else:
            err_message['order_id'] = "Please send 'order_id' key"
    else:
        err_message['customer'] = "Please send 'customer' key"
    if 'settlement_details' in data:
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
    else:
        err_message['settlement_details'] = "Please send 'settlement_details' key"
    if 'tax_detail' in data:
        if type(data['tax_detail']) == list:
            tax_detail = data['tax_detail']
            if len(data['tax_detail']) > 0:
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
    else:
         err_message["tax_detail"] = "Please send 'tax_detail' key"

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
    err_message["Order_Type"] = validation_master_anything(
                data["Order_Type"], "Order Type", alpha_re, 3)
    if any(err_message.values())==True:
        err = {
            "success": False,
            "error" : err_message,
            "message" : "Please correct listed errors!!"
            }
        return err
    else:
        return None







def counter_check(data):
    err_message = {}
    orderdata = {}
    if 'settlement_details' in data:
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
    else:
        err_message['settlement_details'] = "Please send 'settlement_details' key"
   
    if any(err_message.values())==True:
        err = {
            "success": False,
            "error" : err_message,
            "message" : "Please correct listed errors!!"
            }
        return err
    else:
        return None

