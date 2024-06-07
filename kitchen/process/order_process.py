from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from _thread import start_new_thread
from Orders.models import Order, OrderStatusType,QuantityWiseOrderProcess

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, Variant
from kitchen.models import StepToprocess,ProcessTrack
from zapio.settings import Media_Path
from django.db.models import Q
from rest_framework_tracking.mixins import LoggingMixin
# Is Being Prepared

def Order_status_sync(o_id):
	query = Order.objects.filter(id=o_id)
	q = query[0]
	company_id = q.Company_id
	product_status_list = []
	for t in q.order_description:
		p = t['id']
		if t["size"] != "N/A":
			t["v_id"] = \
			Variant.objects.filter(variant__exact=t['size'],Company=company_id)[0].id
		else:
			t["v_id"] = None
		if t["v_id"] == None:
			process_q = ProcessTrack.objects.filter(Q(product=p),~Q(process_status="0"),\
										Q(Order=o_id))
		else:
			process_q = \
			ProcessTrack.objects.filter(Q(product=p),Q(Variant=t["v_id"]),~Q(process_status="0"),\
										Q(Order=o_id))
		if process_q.count()==0:
			product_status_list.append(1)
		else:
			product_status_list.append(2)
	if 2 not in product_status_list:
		orde_status_id = \
		OrderStatusType.objects.filter(Order_staus_name__iexact='Is Being Prepared',active_status=1)[0].id
		query.update(order_status_id=orde_status_id)
	else:
		pass
	return "Order status synchronized properly!!"


class ProcessStartEnd(LoggingMixin,APIView):
	"""
	Process Start/End POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to start/complete the process of products.
		Instruction to Use          : Send "is_start" value as "0" when you are going to start the process and if process is completed send this value as "1".

		Data Post: {
			"p_id"                   : "21",
			"v_id"                 	 : "43",
			"o_id"                   : "2",
			"is_start"               : "1",
			"quan_id"                : "50"
		}

		Response: {

			"success": True, 
			"message": "Process Start/End api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["p_id"] = str(data["p_id"])
			data["v_id"] = str(data["v_id"])
			data["o_id"] = str(data["o_id"])
			data["quan_id"] = str(data["quan_id"])
			err_message = {}

			err_message["p_id"] = \
					validation_master_anything(data["p_id"],
					"Product Id",contact_re, 1)
			err_message["v_id"] = \
					validation_master_anything(data["v_id"],
					"Variant Id",contact_re, 1)
			err_message["o_id"] = \
					validation_master_anything(data["o_id"],
					"Order Id",contact_re, 1)
			err_message["quan_id"] = \
					validation_master_anything(data["quan_id"],
					"Quantty Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			auth_id = request.user.id
			outlet_id = OutletProfile.objects.filter(auth_user=auth_id)
			c_id = outlet_id[0].Company_id
			record = ProcessTrack.objects.filter(Order=data["o_id"],product=data["p_id"],\
							Variant=data["v_id"])
			if record.count()==0:
				return Response({
					"success" : False,
					"message" : "Data not found to process!!"
					})
			else:
				current_time = datetime.now().time()
				if int(data["is_start"]) == 1:
					rec_update =  record.update(started_at=current_time)
					info_msg = "Food making process is started now!!"
				elif int(data["is_start"]) == 0:
					qdata = QuantityWiseOrderProcess.objects.filter(id=data['quan_id'])
					if qdata.count() > 0:
						order_id = qdata[0].order_id
						qdata.update(active_status=1)
						odata = QuantityWiseOrderProcess.objects.filter(\
							order_id=order_id)
						ls =[]
						for i in odata:
							ls.append(i.active_status)
						if False in ls:
							info_msg = "This food is prepared now!!"
						else:
							rec_update =  \
							ProcessTrack.objects.filter(Order=data["o_id"]).\
							update(completed_at=current_time,process_status="0")
							info_msg = "Food is prepared now!!"
					else:
						info_msg = "Data is not valid or food is already processed!!"
					start_new_thread(Order_status_sync, (data["o_id"],))
				else:
					pass
				return Response({
					"success" : True,
					"message" : info_msg
					})
		except Exception as e:
			print("Process Start/End Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
