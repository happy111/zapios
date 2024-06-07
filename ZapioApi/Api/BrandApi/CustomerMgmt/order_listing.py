from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from Orders.models import Order, OrderStatusType,OrderTracking
from Customers.models import CustomerProfile
from django.db.models import Sum,Count,Max
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
from Configuration.models import PaymentMethod



def customer_history(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],mobile=q["mobile"])
	if record[0].has_been_here == 0:
		q["customer_type"] = "New"
	else:
		q["customer_type"] = "Loyal"
	for i in record:
		h_dict = {}
		h_dict["id"] = i.id
		h_dict["order_id"] = i.outlet_order_id
		h_dict["special_instructions"] = i.special_instructions
		t = i.order_time+timedelta(hours=5,minutes=30)
		h_dict["order_time"] = t.strftime("%d/%b/%Y %I:%M %p")
		if i.delivery_time == None:
			h_dict["delivery_time"] = "N/A"
		else:
			d = i.delivery_time+timedelta(hours=5,minutes=30)
			h_dict["delivery_time"] = d.strftime("%d/%b/%Y %I:%M %p")
		h_dict["order_status"] = i.order_status.Order_staus_name
		#h_dict["payment_mode"] = 
		h_dict['color_code'] = i.order_status.color_code
		#h_dict['source'] = 
		q["order_history"].append(h_dict)
	return q



def order_history(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],users_id=q['id'])
	if record[0].has_been_here == 0:
		q["customer_type"] = "New"
	else:
		q["customer_type"] = "Loyal"
	for i in record:
		h_dict = {}
		h_dict["id"] = i.id
		h_dict["log"] = []
		orderlog = OrderTracking.objects.filter(order_id=h_dict["id"]).order_by('id')
		for j in orderlog:
			r_list ={}
			r_list['id'] = j.id
			r_list['status_name'] = j.Order_staus_name.Order_staus_name
			r_list["created_at"] = j.created_at.strftime("%d/%b/%y %I:%M %p")
			h_dict["log"].append(r_list)
		h_dict["order_id"] = i.outlet_order_id
		if i.is_order_now == 0:
			h_dict["order_type"] = 'Schedule Order'
			schedule_time = i.schedule_delivery_time+timedelta(hours=5,minutes=30)
			h_dict["schedule_date"] = schedule_time.strftime("%d/%b/%Y %I:%M %p")
		else:
			h_dict["order_type"] = 'Now'
			h_dict["schedule_date"] = ''
		h_dict["special_instructions"] = i.special_instructions
		t = i.order_time+timedelta(hours=5,minutes=30)
		h_dict["order_time"] = t.strftime("%d/%b/%Y %I:%M %p")

		if i.delivery_time == None or i.delivery_time == '':
			h_dict["delivery_time"] = "N/A"
		else:
			d = i.delivery_time+timedelta(hours=5,minutes=30)
			h_dict["delivery_time"] = d.strftime("%d/%b/%Y %I:%M %p")
		h_dict["order_status"] = i.order_status.Order_staus_name
		if i.settlement_details != None:
			if len(i.settlement_details) > 0:
				h_dict["payment_mode"] = i.settlement_details[0]['payment_name']
			else:
				h_dict['payment_mode'] = ''
		else:
			pm = PaymentMethod.objects.filter(id=i.payment_mode)
			if pm.count() > 0:
				h_dict['payment_mode'] = pm[0].payment_method
			else:
				h_dict['payment_mode'] = ''

		h_dict['color_code'] = i.order_status.color_code
		h_dict['source'] = i.order_source.source_name
		q["order_history"].append(h_dict)
	return q


def pos_order_history(q):
	record = \
	POSOrder.objects.filter(company_id=q["company_id"],customer_number=q["username"])
	if record.count()==0:
		username = "#"+q["username"]
		record = POSOrder.objects.filter(customer_number=username,company_id=q["company_id"])
	else:
		pass
	q["customer_type"] = "N/A"
	for i in record:
		h_dict = {}
		h_dict["id"] = i.id
		h_dict["order_id"] = i.invoice_number
		h_dict["order_time"] = i.created_on.strftime("%d/%b/%Y %I:%M %p")
		h_dict["delivery_time"] = "N/A"
		h_dict["order_status"] = i.status_name
		h_dict["payment_mode"] = i.payment_mode
		h_dict['color_code'] = OrderStatusType.objects.filter(active_status=1).first().color_code
		h_dict['source'] = i.source
		q["order_history"].append(h_dict)
	return q


class CustomerOrders(APIView):
	"""
	Customer Order Listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Order history as per customer.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Order history as per customer api worked well",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Customer Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = CustomerProfile.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Customer data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["company_id"] = record[0].company_id
				q_dict["name"] = record[0].name
				q_dict["email"] = record[0].email
				q_dict["mobile"] = record[0].mobile
				q_dict["order_history"] = []
				q_dict["is_pos"] = record[0].is_pos
				if q_dict["is_pos"] == False:
					history = order_history(q_dict)
				else:
					pass
				final_result.append(history)
			return Response({
						"success": True, 
						"message": "Order history as per customer api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Order history as per customer Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
