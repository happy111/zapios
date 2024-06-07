import json,math,requests
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
from datetime import datetime, timedelta
from Configuration.models import *
from Configuration.models import OrderSource
from Configuration.models import *
from .order_info import *
from geopy.geocoders import Nominatim
from geopy.distance import great_circle


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
    if length < 4:
        aa = 4 - length
        for a in range(aa):
            number = "0" + str(number)
    return str(number)


def FindLatitude(area):
    import requests
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': area,
        'sensor': 'false',
        'region': 'india',
        'key': "AIzaSyCIDUSBqHPfkEssENT_X9vuWt5nzca8_W4"
    }
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    result = res['results'][0]
    if result:
        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']
        return geodata['lat'],geodata['lng']



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
    address_data = postdata["address1"]
    for index in address_data:
        if "type" in index:
            alldata["address_type"] = index["address_type"]
        else:
            pass
        if "address" in index:
            alldata["address"] = index["address"]
            if alldata['address'] != '':
                latitude,longitude = FindLatitude(alldata["address"])
                alldata['latitude'] = latitude
                alldata['longitude'] = longitude
                if (
                    alldata["latitude"] != None
                    and alldata["longitude"] != None
                    and alldata["latitude"] != ""
                    and alldata["longitude"] != ""
                    and outletdetails.latitude != None
                    and outletdetails.longitude != None
                    and outletdetails.latitude != ""
                    and outletdetails.longitude != ""
                    and outletdetails.latitude != "undefined"
                    and outletdetails.longitude != "undefined"
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
                            print(order_serializer.errors)
                else:
                    pass
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

    od_data = orderdata.customer
    alldata["first_name"]           = od_data["first_name"]
    alldata["last_name"]            = od_data["last_name"]
    alldata["mobile"]               = od_data["mobile"]
    alldata["company"]              = orderdata.Company.id
    chkuser = CustomerProfile.objects.filter(
        Q(mobile=alldata["mobile"]), Q(company=alldata["company"])
    )
    if chkuser.count() > 0:
        a = {}
        cadr    = chkuser[0].address1
        chka    = address_data[0]["address"]
        loc     = address_data[0]["locality"]
        result = []
        flag = 1
        for k in cadr:
            if k["address"] == chka:
                flag = 0
            else:
                pass
        if flag == 1:
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
        source_data = OrderSource.objects.filter(id=str(postdata['Order_Source']))[0].source_name
        if source_data == 'Counter':
            return 'success'
        cust_data = {}
        cust_data["mobile"] = alldata["mobile"]
        cust_data["company"] = alldata["company"]
        cust_data["address1"] = postdata["address1"]
        cust_data["latitude"] = alldata["latitude"]
        cust_data["longitude"] = alldata["longitude"]
        cust_data["first_name"] = postdata["customer"]["first_name"]
        cust_data["last_name"] = postdata["customer"]["last_name"]
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
            print(customer_registration_serializer.errors)
    return "Success"

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
        data["customer"]["first_name"] = customer["first_name"]
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

class OrderProcess(LoggingMixin, APIView):
    """
	Customer Order POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to save all order related
		data to store it in database for future reference.

		Data Post:  {
			"customer": {
							"name": "umesh",
							"mobile": "8423845784",
							"email" : "umeshsamal3@gmail.com",
                            "order_id" : "ewrewrwer"
						},
                    "address1":[
                        {
                                
                            "longitude":77.20988899999999,
                            "latitude":28.5429549,
                            "address":"Hari Nagar",
                            "locality": "110",
                            "state":"delhi",
                            "address_type":"home",
                            "city": "2"
                                
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
			
            "delivery_time":"",
            "delivery_instructions":"",
            "company_id":13,
            "Company_outlet_details":"",
            "order_time":"2020-10-23T09:14:44.183Z",
            "taxes":50,
            "payment_mode":9,
            "payment_id":"pay_FrUwIdWZ4gbYjb",
            "Payment_status":1,
            "special_instructions":"",
            "sub_total":1925,
            "cart_discount":0,
            "total_bill_value":2021,
            "total_items":3,
            "outlet_id" : 64,
            "coupon_code":0,
            "Delivery_Charge":0,
            "Order_Type": "takeaway",
            "is_order_now":1,
            "Payment_source":4,
            "Order_Source" : 4,
            "Packing_Charge":0,
            "discount_name": "",
            "discount_reason": "",
             "tax_detail"  :
              [
                 {
                    "id": "9",
                    "tax_amount"  : "50"
                  }
              ],
		
		}

		Response: {

			"success": true,
			"message": "Order Received successfully"
		}

	"""
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            data = request.data
            orderdata = {}
            user = request.user
            err_message = {}
            err_message["order source"] = \
                    validation_master_anything(str(data["Order_Source"]),
                    "Order Source",contact_re, 1)
            source_data = OrderSource.objects.filter(id=str(data['Order_Source']))[0].source_name
            co_id = OutletProfile.objects.filter(id=data['outlet_id'])[0].Company_id
            if source_data == 'Swiggy':
                validation_check = swiggy_check(data)
                if validation_check != None:
                    return Response(validation_check)
                orderdata["Company"] = co_id
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
                orderdata["order_id"] = sn + last_id
                orderdata["address"] = data["address1"]
                orderdata["customer"] = data["customer"]
                if "mobile" in data["customer"]:
                    orderdata["mobile"] = data["customer"]["mobile"]
                else:
                    orderdata["mobile"] = "" 
            elif source_data == 'Zomato':
                validation_check = zomato_check(data)
                if validation_check != None:
                    return Response(validation_check)
                orderdata["Company"] = co_id
                orderdata["customer"] = data["customer"]
                


                if outlet_wise_order_count > 0:
                    final_outlet_wise_order_count = int(outlet_wise_order_count) + 1
                else:
                    final_outlet_wise_order_count = 1
                
                a = genrate_invoice_number(final_outlet_wise_order_count)
                finalorderid = str(sn) + str(out_id) + "-" + str(2021) + str(a)
                orderdata["order_id"] = sn + last_id
                


                orderdata["address"] = data["address1"]
                orderdata["customer"] = data["customer"]
                if "mobile" in data["customer"]:
                    orderdata["mobile"] = data["customer"]["mobile"]
                else:
                    orderdata["mobile"] = "" 
            elif source_data == 'Phone' or source_data == 'Website Order':
                validation_check = phone_check(data)
                if validation_check != None:
                    return Response(validation_check) 
                orderdata["Company"] = co_id
                orderdata["customer"] = data["customer"]
                now = datetime.now()
                today = now.date()
                last_id_q = Order.objects.filter(order_time__date__gte=today).last()
                if last_id_q:
                    last_id = str(last_id_q.id)
                else:
                    last_id = "001"
                today_date = str(today).replace('-',"")
                sn = 'VirtualKitchen2'
                outlet_wise_order_count = Order.objects.filter(
                    order_time__date__gte=today).count()
                if outlet_wise_order_count > 0:
                    final_outlet_wise_order_count = int(outlet_wise_order_count) + 1
                else:
                    final_outlet_wise_order_count = 1
               
                a = genrate_invoice_number(final_outlet_wise_order_count)
               
                finalorderid = str(today_date) +str(a)
                

                orderdata["order_id"] = sn + finalorderid
                



                orderdata["address"] = data["address1"]
                orderdata["customer"] = data["customer"]
                if "mobile" in data["customer"]:
                    orderdata["mobile"] = data["customer"]["mobile"]
                else:
                    orderdata["mobile"] = ""

            elif source_data == 'Counter':
                validation_check = counter_check(data)
                if validation_check != None:
                    return Response(validation_check)
                orderdata["Company"] = co_id
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
                orderdata["order_id"] = sn + last_id
                orderdata["address"] = data["address1"]
                orderdata["customer"] = data["customer"]
                if "mobile" in data["customer"]:
                    orderdata["mobile"] = data["customer"]["mobile"]
                else:
                    orderdata["mobile"] = "" 
            else:
                pass
            company_query = Company.objects.filter(id=co_id)
            orderdata["Company"] = co_id
            orderdata["order_description"] = data["order_description"]
            orderdata["user"] = ManagerProfile.objects.filter(auth_user_id=user.id)[
                0
            ].username
            company_name = company_query[0].company_name
            orderdata["order_id"] =  orderdata["order_id"] 
            orderdata["outlet_order_id"] = finalorderid
            orderdata["order_time"] = datetime.now()
            orderdata["taxes"] = data["taxes"]
            orderdata["delivery_instructions"] = data["delivery_instructions"]
            orderdata["special_instructions"] = data["special_instructions"]
            # orderdata["note"] = data["note"]

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
            orderdata["tax_detail"] = data["tax_detail"]
            if 'coupon_code' in data:
                orderdata["coupon_code"] = data["coupon_code"]
            now = datetime.now()
            orderdata["day"] = now.strftime("%A")
            order_serializer = OrderSerializer(data=orderdata)
            if order_serializer.is_valid():
                order_obj = order_serializer.save()
                orderid = order_serializer.data["id"]
                oid = order_serializer.data["order_id"]
                start_new_thread(order_registration_notification, (orderid, oid,data))
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
                    used_coupon["Company"] = co_id
                    used_coupon["created_at"] = datetime.now()
                    used_coupon["outlet"] = data['outlet_id']
                    usedcoupon_serializer = CouponUsedSerializer(data=used_coupon)
                    if usedcoupon_serializer.is_valid():
                        usedcoupon_serializer.save()
                    else:
                        return Response(
                            {
                                "success": False,
                                "message": str(usedcoupon_serializer.errors),
                            }
                        )
                user_data = ManagerProfile.objects.filter(auth_user_id=request.user.id)
                key_person = user_data[0].username
                order_tracking = OrderTracking.objects.create(
                    order_id=orderid,
                    Order_staus_name_id=orderdata["order_status"],
                    created_at=datetime.now(),
                    key_person=key_person
                )


                order_id = orderdata["order_id"]
                status = Order_status_q[0].Order_staus_name
                # start_new_thread(order_sms_notification, (order_id, status))
                data_info = OrderInfo(orderid)
                print("SMS Passed.")
                return Response(
                    {"success": True, 
                      "data"  : data_info,
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

