import re,os
from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ZapioApi.api_packages import *
from datetime import datetime

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from UserRole.models import ManagerProfile,UserType
from rest_framework import serializers
from Customers.models import CustomerProfile
from Orders.models import Order
from datetime import datetime, timedelta
from Product.models import *


def customer_history(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],mobile=q["mobile"]).order_by('-id')
	for i in record:
		h_dict = {}
		h_dict["id"] = i.id
		h_dict["order_id"] = i.outlet_order_id
		h_dict["order_description"] = i.order_description
		h_dict["total_value"] = i.total_bill_value
		h_dict["special_instructions"] = i.special_instructions
		t = i.order_time+timedelta(hours=5,minutes=30)
		h_dict["order_time"] = t.strftime("%d/%b/%Y %I:%M %p")
		if i.delivery_time == None:
			h_dict["delivery_time"] = "N/A"
		else:
			d = i.delivery_time+timedelta(hours=5,minutes=30)
			h_dict["delivery_time"] = d.strftime("%d/%b/%Y %I:%M %p")
		h_dict["order_status"] = i.order_status.Order_staus_name
		h_dict['color_code'] = i.order_status.color_code
		q["order_history"].append(h_dict)
	return q

def countTag(q):
	tag = []
	totaltag = 0
	record = \
	Order.objects.filter(Company_id=q["company_id"],users_id=q['id'])
	if record.count() > 0:
		for index in record:
			order_description = index.order_description
			for k in order_description:
				if 'id' in k:
					product_data = Product.objects.filter(id=k['id'])
					print("umeshsamal",product_data.count())
					if product_data.count() > 0:
						alltag = product_data[0].tags
						if alltag != None:
							if len(alltag) > 0:
								for index in alltag:
									name = Tag.objects.filter(id=index)[0].tag_name
									tag.append(name)
								totaltag = totaltag + len(alltag)
	return totaltag,tag

def healthCheck(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],users_id=q['id'])
	first_order = record[0].order_time
	last_order = record.last().order_time
	now = datetime.now()
	todate = now.date()
	date_format = "%Y-%m-%d"
	a = str(last_order)
	x = a.split(" ")
	lorder = x[0]
	t1 = datetime.strptime(str(lorder),date_format)
	t2 = datetime.strptime(str(todate),date_format)
	di = t2 - t1
	d =di.days
	chealth =''
	if d >= 365:
		chealth = 'Lost'
	elif d >= 181 and d < 365:
		chealth = 'Alert'
	elif d >= 91 and d < 181:
		chealth = 'Warning'
	elif d >= 61 and d < 91:
		chealth = 'At Risk'
	elif d >= 31 and d < 61:
		chealth = 'Drifting'
	elif d >= 16 and d < 31:
		chealth = 'Good'
	elif d >= 0 and d < 16:
		chealth = 'Great'
	return chealth



class CustomerWiseOrder(APIView):
	"""
	Order retrieval POST API

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
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user
			data["id"] = str(data["id"])
			co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"], "Customer ID",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = CustomerProfile.objects.filter(company__id=co_id,id=data['id'])
			print("vvvvvvvvvvvvvv",record.count())
			if record.count() == 0:
				return Response(
				{
					"success": True,
 					"message": "Required Customer data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["company_id"] = record[0].company_id
				q_dict["first_name"] = record[0].first_name
				q_dict['last_name'] = record[0].last_name
				q_dict["email"] = record[0].email
				q_dict["mobile"] = record[0].mobile
				q_dict["address"] = record[0].address
				q_dict["other_address"] = record[0].address1
				
				print("vvvvvvvvvvvvvvv",q_dict)

				aa = Order.objects.filter(Company_id=q_dict["company_id"],\
					                users_id=record[0].id).order_by('id')
				
				if aa.count() > 20:
					q_dict["customer_type"] = "Champions"
				elif aa.count() >= 10 and aa.count() < 20:
					q_dict["customer_type"] = "Extremely Loyal"
				elif aa.count() >= 6 and aa.count() < 10:
					q_dict["customer_type"] = "Loyal"
				elif aa.count() >= 4 and aa.count() < 6:
					q_dict["customer_type"] = "Regular"
				elif aa.count() == 3:
					q_dict["customer_type"] = "Frequent"
				elif aa.count() == 2:
					q_dict["customer_type"] = "Promising"
				elif aa.count() == 1:
					q_dict["customer_type"] = "New"
				else:
					q_dict["customer_type"] = "Undefined"
				
				if aa.count() > 0:
					chk_health = healthCheck(q_dict)
					

					q_dict["chkhealth"] = chk_health
					customer_tag,tag = countTag(q_dict)
					
					print("nnnnnnnnnnnnnnnn",customer_tag, tag)

					q_dict["totaltag"] = customer_tag
					s = set(tag)
					q_dict["tag"] = list(s)
					order_result = aa.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
					q_dict["total_spent"] = order_result[0]['total_revenue']
					t =  aa.last().order_time+timedelta(hours=5,minutes=30)
					q_dict["last_order"] = t.strftime("%d-%b-%Y %I:%M %p")
					q_dict["invoice_number"] = aa.last().order_id
					q_dict["product_detail"] = []
					product_detail = aa.last().order_description
					for i in product_detail:
						dic = {}
						dic['product_name'] = i['name']
						dic['qty'] = i['quantity']
						if 'size' in i:
							dic['size'] = i['size']
						else:
							pass
						q_dict["product_detail"].append(dic)
					q_dict["total_value"] = aa.last().total_bill_value
				else:
					q_dict["chkhealth"] = 'Lost'
					q_dict["totaltag"] = 0
					q_dict["total_spent"] = 0
				
				q_dict["order_history"] = []
				history = customer_history(q_dict)
				final_result.append(history)
			return Response({
						"success": True, 
						"message": "Order history as per customer api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Profile update updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})