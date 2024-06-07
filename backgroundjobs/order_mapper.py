from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType,OrderTracking
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
import secrets
from Product.models import Addons





def items_description():
	urban_record = UrbanOrders.objects.all()
	for i in urban_record:
		main_order = Order.objects.filter(urban_order_id=i.order_id)
		if main_order.count()!=0:
			order_schema = {}
			order_schema["order_description"] = []
			urban_order_details = i.order_description
			for i in urban_order_details:
				order_dict = {}
				order_dict["id"] = i["id"]
				order_dict["name"] = i["title"]
				order_dict["price"] = i["total"]
				order_dict["quantity"] = i["quantity"]
				merchant_id = i["merchant_id"]
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
				final_product_id = merchant_id.replace('I-','')
				order_dict["final_product_id"] =  final_product_id
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
			order_update = main_order.update(order_description=order_schema["order_description"])
		else:
			pass



def delete_orders():
	record = \
	Order.objects.filter(Q(outlet_id=33)|Q(outlet_id=34)|Q(outlet_id=35)|Q(outlet_id=None))
	for i in record:
		track_delete = OrderTracking.objects.filter(order=i.id).delete()
	record_delete = record.delete()


def delete_one():
	record = \
	Order.objects.filter(id=989)
	for i in record:
		track_delete = OrderTracking.objects.filter(order=i.id).delete()
	record_delete = record.delete()


