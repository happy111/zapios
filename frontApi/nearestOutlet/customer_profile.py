import calendar
from datetime import datetime
from django.db.models import Q
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from rest_framework_tracking.mixins import LoggingMixin
from datetime import datetime, timedelta
import time
from Orders.models import *

class CustomeProfile(LoggingMixin, APIView):
	"""
	Schedule order  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to profile details.

		Data Post: {

			"email"	    :	"umeshsamal3@gmail.com",


		}

		Response: {

			"status"				: True,

		}

	"""
	def post(self,request):
		try:
			data = request.data
			cust_data = CustomerProfile.objects.filter(email = data['email'],company_id = data['Company'])
			final_result = []
			if cust_data.count() > 0:
				order_data = Order.objects.filter(users_id=cust_data[0].id)
				if order_data.count() > 0:
					p_list = {}
					p_list['name'] = cust_data[0].name
					p_list['mobile'] = cust_data[0].mobile
					p_list['email'] = cust_data[0].email
					
					# p_list['address'] = []
					# adress_data = cust_data[0].address1
					# for k in adress_data:
					# 	di = {}
					# 	di['first_name'] = cust_data[0].name.split(' ')[0]
					# 	if len(cust_data[0].name.split(' ')) > 2:
					# 		di['last_name'] = cust_data[0].name.split(' ')[1]
					# 	else:
					# 		di['last_name'] = ''
					# 	di['email'] = cust_data[0].email
					# 	di['phone'] = cust_data[0].mobile
					# 	if 'city' in k:
					# 		di['city']  = k['city']
					# 	else:
					# 		di['city'] = ''
					# 	if 'state' in k:
					# 		di['state']  = k['state']
					# 	else:
					# 		di['state'] = ''
					# 	if 'address' in k:
					# 		di['address'] = k['address']
					# 	else:
					# 		di['address'] = ''
						
					# 	if 'pincode' in k:
					# 		di['pincode'] = k['pincode']
					# 	else:
					# 		di['pincode'] = ''
					# 	di['locality'] = k['locality']
					# 	di['address_type'] = k['address_type']
					# 	p_list['address'].append(di)

					p_list['order'] = []
					total = 0 
					for index in order_data:
						q_list = {}
						q_list["address"] = 	index.address
						q_list["order_description"] = 	index.order_description
						q_list["sub_total"]      = 			index.sub_total
						q_list["discount_value"] =      index.discount_value
						q_list["total_bill_value"] = round(index.total_bill_value,2)
						q_list["discount_name"] = index.discount_name
						q_list["delivery_instructions"] = index.delivery_instructions
						q_list["delivery_charge"] = index.delivery_charge
						q_list["packing_charge"] = index.packing_charge
						q_list["order_id"] = index.outlet_order_id
						order_time = index.order_time + timedelta(hours=5, minutes=30)
						q_list["order_time"] = order_time.strftime("%d/%b/%y %I:%M %p")
						total = total + float(index.total_bill_value)
						p_list['order'].append(q_list)
					p_list['total'] = round(total,2)
					p_list['order_count'] = order_data.count()
					final_result.append(p_list)
				else:
					pass
			return Response({
				"success": True,
				"data"   : final_result,
			   })
		except Exception as e:
			print(e)