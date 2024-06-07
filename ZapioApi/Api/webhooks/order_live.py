from rest_framework.views import APIView
from rest_framework.response import Response
import json
from datetime import datetime
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, RawApiResponse, UrbanOrders, ProductSync
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from Orders.models import Order, OrderTracking
from Location.models import *
from Outlet.models import OutletProfile
from django.db.models import Q
from Product.models import Product

class UrbanOrdersSerializer(serializers.ModelSerializer):
	class Meta:
		model = UrbanOrders
		fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'


def genrate_invoice_number(number):
	length = len(str(number))
	if length < 6:
		aa = 6 - length
		for a in range(aa):
			number = "0" + str(number)
	return str(number)


class LiveOrders(LoggingMixin, APIView):
	"""
	Outletwise LIVE orders Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for order relay in urbanpiper.

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			store_info = data["order"]["store"]
			outlet_id = store_info["merchant_ref_id"]
			outlet_check = OutletSync.objects.filter(outlet=outlet_id,sync_status="synced",\
																outlet__active_status=1)
			if outlet_check.count() == 0:
				return Response({
					"success" : False,
					"message" : "Outlet is not valid!!"
					})
			else:
				pass
			company_id = outlet_check[0].company_id
			sync_outlet_id = outlet_check[0].id
			raw_record_create = \
			OrderRawApiResponse.objects.create(company_id=company_id,sync_outlet_id=sync_outlet_id,\
				api_response=data)
			order_data = {}
			order_data["customer_data"] = {}
			order_data["customer_data"]["email"] = data["customer"]["email"]
			order_data["customer_data"]["name"] = data["customer"]["name"]
			order_data["customer_data"]["mobile_number"] = data["customer"]["phone"]
			order_data["customer_address"] = data["customer"]["address"]
			order_data["order_id"] = data["order"]["details"]["id"]
			order_data["source"] = data["order"]["details"]["channel"]
			order_data["next_states"] = data["order"]["next_states"]
			order_data["next_expected_state"] = data["order"]["next_states"]
			order_data["order_state"] = data["order"]["details"]["order_state"]
			order_data["order_description"] = data["order"]["items"]
			order_data["final_payment"] = data["order"]["payment"]
			order_data["coupon_code"] = data["order"]["details"]["coupon"]
			order_data["channel_order_id"] = data["order"]["details"]["ext_platforms"][0]["id"]
			order_data["Company"] = company_id
			order_data["outlet"] = outlet_id
			order_data["discount_value"] = data["order"]["details"]["discount"]
			order_data["payment_id"] = data["order"]["payment"][0]['srvr_trx_id']
			order_data["order_level_total_taxes"] = \
			data["order"]["details"]["order_level_total_taxes"]
			order_data["total_tax"] = \
			data["order"]["details"]["total_taxes"]
			order_data["order_level_total_charges"] = \
			data["order"]["details"]["order_level_total_charges"]
			order_data["item_level_total_charges"] = \
			data["order"]["details"]["item_level_total_charges"]
			order_data["item_level_total_taxes"] = \
			data["order"]["details"]["item_level_total_taxes"]
			order_data["order_type"] = \
			data["order"]["details"]["order_type"]
			order_data["sub_total"] = \
			data["order"]["details"]["order_subtotal"]
			order_data["total_bill_value"] = \
			data["order"]["details"]["order_total"]
			order_data["special_instructions"] = \
			data["order"]["details"]["instructions"]
			total_items = 0
			discount_value = 0
			# sub_total = 0
			total_bill_value = 0
			for i in order_data["order_description"]:
				discount_value = discount_value+i["discount"]
				total_items = total_items + i["quantity"]
			order_data["total_items"] = total_items
			# order_data["discount_value"] = discount_value

			ureban_order_record = \
			UrbanOrders.objects.filter(order_id=order_data["order_id"])
			if ureban_order_record.count() == 0:
				serializer = UrbanOrdersSerializer(data=order_data)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print(str(serializer.errors))
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response({
						"success": False, 
						"message": "Order is already placed!!",
						})
			query = ureban_order_record[0]
			delivery_type = data["order"]["details"]["ext_platforms"][0]["delivery_type"]
			aggregator_payment_mode = data["order"]["payment"][0]['option']
			order_schema = {}
			if delivery_type == "partner":
				order_schema["delivery_type"] = "Partner"
			else:
				order_schema["delivery_type"] = "Self"
			if aggregator_payment_mode == "payment_gateway" and order_data["source"] == "zomato":
				order_schema["aggregator_payment_mode"] = "Zomato"
			elif order_data["source"] == "zomato" and aggregator_payment_mode != "payment_gateway":
				order_schema["aggregator_payment_mode"] = "COD"
			else:
				order_schema["aggregator_payment_mode"] = "Swiggy"
			order_schema["outlet"] = query.outlet_id
			order_schema["Company"] = query.Company_id
			order_schema["taxes"] = query.total_tax
			order_schema["total_bill_value"] = query.total_bill_value
			order_schema["special_instructions"] = query.special_instructions
			order_schema["channel_order_id"] = query.channel_order_id
			order_schema["discount_value"] = query.discount_value
			urban_order_details = query.order_description
			order_schema["order_description"] = []
			for i in urban_order_details:
				order_dict = {}
				order_dict["id"] = i["id"]
				order_dict["name"] = i["title"]
				order_dict["price"] = i["total"]
				order_dict["quantity"] = i["quantity"]
				merchant_id = i["merchant_id"]
				final_product_id = merchant_id.replace('UP-','')
				order_dict["final_product_id"] =  final_product_id
				order_dict["tax_detail"] = []
				cgst = {}
				cgst["id"] = 1
				cgst["tax_name"] = "CGST | 2.5"
				cgst["tax_percent"] = 2.5
				cgst["tax_value"] = i["taxes"][0]["value"]
				order_dict["tax_detail"].append(cgst)
				sgst = {}
				sgst["id"] = 2
				sgst["tax_name"] = "SGST | 2.5"
				sgst["tax_percent"] = 2.5
				sgst["tax_value"] = i["taxes"][1]["value"]
				order_dict["tax_detail"].append(sgst)
				final_record = \
				ProductSync.objects.filter(id=final_product_id)
				if final_record.count() == 0:
					kot_desc = ""
				else:
					kot_desc = final_record[0].product.kot_desc
				order_dict["kot_desc"] = kot_desc
				if i["food_type"] == "1":
					order_dict["food_type"] = "Vegetarian"
				else:
					order_dict["food_type"] = "Non Vegetarian"
				order_dict["size"] = ""
				order_dict["add_ons"] = i["options_to_add"]
				for j in i["options_to_add"]:
					merchant_id = j["merchant_id"]
					final_addon_id = merchant_id.replace('A-','')
					j["final_addon_id"] = final_addon_id
				order_schema["order_description"].append(order_dict)
			order_schema["address"] = {}
			urban_address = query.customer_address
			order_schema["address"]["city"] = urban_address["city"]
			if urban_address["line_1"] == None:
				urban_address["line_1"] = "N/A"
			else:
				pass
			if urban_address["line_2"] == None:
				urban_address["line_2"] = "N/A"
			else:
				pass
			if urban_address["landmark"] == None:
				urban_address["landmark"] = "N/A"
			else:
				pass
			order_schema["address"]["address"] = urban_address["line_1"]+" "+urban_address["line_2"]\
														+" "+urban_address["landmark"]
			order_schema["address"]["latitude"] = urban_address["latitude"] 
			order_schema["address"]["longitude"] = urban_address["longitude"]
			order_schema["address"]["locality"] = urban_address["sub_locality"]
			order_schema["is_aggregator"] = 1
			order_schema["coupon_code"] = query.coupon_code
			order_schema["total_items"] = query.total_items
			order_schema["order_source"] = query.source
			order_schema["Aggregator_order_status"] = query.order_state
			order_schema["urban_order_id"] = query.order_id
			order_schema["customer"] = query.customer_data
			order_schema["order_status"] = 1
			order_schema["order_time"] = query.created_at
			order_schema["discount_value"] = query.discount_value
			order_schema["sub_total"] = query.sub_total
			order_schema["order_type"] = 	query.order_type
			order_record = Order.objects.filter(Company=order_schema['Company'])
			if order_record.count() != 0:
				is_visited = order_record.\
				filter(customer__mobile_number=order_schema['customer']['mobile_number'])
				if is_visited.count() == 0:
					pass
				else:
					order_schema['has_been_here'] = 1
					is_visited.update(has_been_here=1)
			else:
				pass
			last_id_q = Order.objects.filter(Company_id=order_schema["Company"]).last()
			if last_id_q:
				last_id = str(last_id_q.id+1)
			else:
				last_id = '001'
			last_oid_q = Order.objects.filter(outlet_id=order_schema["outlet"]).last()
			city = OutletProfile.objects.filter(id=order_schema["outlet"])[0].city_id
			state = CityMaster.objects.filter(id=city)[0].state_id
			sn = StateMaster.objects.filter(id=state)[0].short_name
			out_id = order_schema["outlet"]
			outlet_wise_order_count = \
			Order.objects.filter(Q(Company_id=order_schema["Company"]),\
								Q(outlet_id=order_schema["outlet"])).count()
			if outlet_wise_order_count > 0:
				final_outlet_wise_order_count = int(outlet_wise_order_count) + 1
			else:
				final_outlet_wise_order_count = 1
			a = \
			genrate_invoice_number(final_outlet_wise_order_count)
			finalorderid = str(sn)+''+str(out_id)+'-'+str(2021)+''+str(a)
			order_schema['outlet_order_id'] = finalorderid
			company_name = query.Company.company_name
			order_schema['order_id'] = company_name+last_id
			main_order = Order.objects.filter(urban_order_id=order_schema["urban_order_id"])
			if main_order.count() == 0:
				order_serializer = OrderSerializer(data=order_schema)
				if order_serializer.is_valid():
					data_info = order_serializer.save()
					order_tracking = \
					OrderTracking.objects.create(order_id=data_info.id, 
						Order_staus_name_id=order_schema['order_status'], created_at=datetime.now())
				else:
					print(str(order_serializer.errors))
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(order_serializer.errors),
						})
			else:
				pass
			return Response({
						"success": True, 
						"message": "Order Relay webhook mechanism api worked well!!"
						})
		except Exception as e:
			print("Order Relay webhook mechanism Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



