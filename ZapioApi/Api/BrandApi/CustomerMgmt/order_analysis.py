from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from Orders.models import Order
from Customers.models import CustomerProfile
from django.db.models import Sum,Count,Max
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
from Location.models import *


def order_analysis(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],users_id=q["id"])
	first_order = record[0].order_time
	last_order = record.last().order_time
	q["first_order"] = first_order.strftime("%d/%b/%Y %I:%M %p")
	q["last_order"] = last_order.strftime("%d/%b/%Y %I:%M %p")
	q["total_order"] = record.count()
	total_spent = record.aggregate(Sum('total_bill_value'))
	q["total_spent"] = total_spent['total_bill_value__sum']
	q["order_avg"] = round(q["total_spent"]/q["total_order"],2)
	q_pre_outlet = record.values('outlet').annotate(visit_count=Count('outlet'))
	visited_outlet = {}
	for i in q_pre_outlet:
		visited_outlet[i["outlet"]] = i["visit_count"]
	outlet_id = max(visited_outlet, key=visited_outlet.get) 
	q["preferred_outlet"] = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
	day_diff = (last_order.date()-first_order.date()).days
	if day_diff != 0:
		q["order_pattern"] = str(round(day_diff/q["total_order"],2))+" days"
	else:
		q["order_pattern"] = "First Order"

	now = datetime.now()
	a = datetime.today().date()
	first_day = a.replace(day=1)
	yesterday = now - timedelta(days=7)
	last_week_day = now - timedelta(days=7)
	order_record = Order.objects.filter(Company_id=q["company_id"],users_id=q["id"],order_time__gte=yesterday)
	if order_record.count() > 0:
		revenue_result = order_record.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
		q['before_7'] = revenue_result[0]['total_revenue']
	else:
		q['before_7'] = ''
	order_records = Order.objects.filter(Company_id=q["company_id"],users_id=q["id"])
	if order_records.count() > 0:
		revenue_results = order_records.values('Company').\
								annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))

		q['life_time_value'] = revenue_results[0]['total_revenue']
	else:
		q['life_time_value'] =''
	return q


def healthCheck(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],customer__mobile_number=q["mobile"])
	if record.count() > 0:
		first_order = record[0].order_time
		last_order = record.last().order_time
		q["first_order"] = first_order.strftime("%d/%b/%Y %I:%M %p")
		q["last_order"] = last_order.strftime("%d/%b/%Y %I:%M %p")
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
	else:
		d = 0
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
	else:
		chealth = 'Lost'

	return chealth

def scoreCheck(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],customer__mobile_number=q["mobile"])
	if record.count() > 0:
		first_order = record[0].order_time
		last_order = record.last().order_time
		q["first_order"] = first_order.strftime("%d/%b/%Y %I:%M %p")
		q["last_order"] = last_order.strftime("%d/%b/%Y %I:%M %p")
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
	else:
		d = 0
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
	else:
		chealth = 'Lost'

	aa = Order.objects.filter(Company_id=q["company_id"],\
									customer__mobile_number=q["mobile"])
	customer_type = ''
	if aa.count() > 20:
		customer_type = "Champions"
	elif aa.count() >= 10 and aa.count() < 20:
		customer_type = "Extremely Loyal"
	elif aa.count() >= 6 and aa.count() < 10:
		customer_type = "Loyal"
	elif aa.count() >= 4 and aa.count() < 6:
		customer_type = "Regular"
	elif aa.count() == 3:
		customer_type = "Frequent"
	elif aa.count() == 2:
		customer_type = "Promising"
	elif aa.count() == 0:
		customer_type = "New"
	else:
		customer_type = "Undefined"


	customer_score = ''
	if chealth=='Great' and customer_type=='Champions':
		customer_score = 100
	elif chealth=='Great' and customer_type=='Extremely Loyal':
		customer_score = 90
	elif chealth=='Great' and customer_type=='Loyal':
		customer_score = 80
	elif chealth=='Great' and customer_type=='Regular':
		customer_score = 75
	elif chealth=='Great' and customer_type=='Frequent':
		customer_score = 70
	elif chealth=='Great' and customer_type=='Promising':
		customer_score = 65
	elif chealth=='Great' and customer_type=='New':
		customer_score = 60
	elif chealth=='Good' and customer_type=='Champions':
		customer_score = 86
	elif chealth=='Good' and customer_type=='Extremely Loyal':
		customer_score = 77
	elif chealth=='Good' and customer_type=='Loyal':
		customer_score = 69
	elif chealth=='Good' and customer_type=='Regular':
		customer_score = 64
	elif chealth=='Good' and customer_type=='Frequent':
		customer_score = 60
	elif chealth=='Good' and customer_type=='Promising':
		customer_score = 56
	elif chealth=='Good' and customer_type=='New':
		customer_score = 51
	elif chealth=='Drifting' and customer_type=='Champions':
		customer_score = 73
	elif chealth=='Drifting' and customer_type=='Extremely Loyal':
		customer_score = 66
	elif chealth=='Drifting' and customer_type=='Loyal':
		customer_score = 59
	elif chealth=='Drifting' and customer_type=='Regular':
		customer_score = 55
	elif chealth=='Drifting' and customer_type=='Frequent':
		customer_score = 51
	elif chealth=='Drifting' and customer_type=='Promising':
		customer_score = 48
	elif chealth=='Drifting' and customer_type=='New':
		customer_score = 44
	elif chealth=='At Risk' and customer_type=='Champions':
		customer_score = 63
	elif chealth=='At Risk' and customer_type=='Extremely Loyal':
		customer_score = 57
	elif chealth=='At Risk' and customer_type=='Loyal':
		customer_score = 50
	elif chealth=='At Risk' and customer_type=='Regular':
		customer_score = 47
	elif chealth=='At Risk' and customer_type=='Frequent':
		customer_score = 44
	elif chealth=='At Risk' and customer_type=='Promising':
		customer_score = 41
	elif chealth=='At Risk' and customer_type=='New':
		customer_score = 38
	elif chealth=='Warning' and customer_type=='Champions':
		customer_score = 54
	elif chealth=='Warning' and customer_type=='Extremely Loyal':
		customer_score = 49
	elif chealth=='Warning' and customer_type=='Loyal':
		customer_score = 43
	elif chealth=='Warning' and customer_type=='Regular':
		customer_score = 40
	elif chealth=='Warning' and customer_type=='Frequent':
		customer_score = 38
	elif chealth=='Warning' and customer_type=='Promising':
		customer_score = 35
	elif chealth=='Warning' and customer_type=='New':
		customer_score = 32
	elif chealth=='Alert' and customer_type=='Champions':
		customer_score = 46
	elif chealth=='Alert' and customer_type=='Extremely Loyal':
		customer_score = 42
	elif chealth=='Alert' and customer_type=='Loyal':
		customer_score = 37
	elif chealth=='Alert' and customer_type=='Regular':
		customer_score = 35
	elif chealth=='Alert' and customer_type=='Frequent':
		customer_score = 32
	elif chealth=='Alert' and customer_type=='Promising':
		customer_score = 30
	elif chealth=='Alert' and customer_type=='New':
		customer_score = 28
	elif chealth=='Lost' and customer_type=='Champions':
		customer_score = 40
	elif chealth=='Lost' and customer_type=='Extremely Loyal':
		customer_score = 36
	elif chealth=='Lost' and customer_type=='Loyal':
		customer_score = 32
	elif chealth=='Lost' and customer_type=='Regular':
		customer_score = 30
	elif chealth=='Lost' and customer_type=='Frequent':
		customer_score = 28
	elif chealth=='Lost' and customer_type=='Promising':
		customer_score = 26
	elif chealth=='Lost' and customer_type=='New':
		customer_score = 24
	elif chealth=='Null' and customer_type=='Undefined':
		customer_score = 0
	else:
		pass

	return customer_score


class OrderAnalysis(APIView):
	"""
	AddonDetails retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Order analysis as per customer data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Order analysis as per customer retrieval api worked well",
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
				q_dict["address"] = []
				if len(record[0].address1) > 0:
					for index in record[0].address1:
						dic = {}
						if 'city' in index:
							try:
								city = int(index["city"])
								city_data = CityMaster.objects.filter(id=index['city'])
								if city_data.count() > 0:
									dic['city'] = city_data[0].city
								else:
									dic['cuty'] = index['city']
							except Exception as e:
								dic['cuty'] = index['city']
						if 'locality' in index:
							try:
								locality = int(index["locality"])
								city_data = CityMaster.objects.filter(id=index['city'])
								locality_data = AreaMaster.objects.filter(id=index['locality'])
								if locality_data.count() > 0:
									dic['locality'] = locality_data[0].area
								else:
									dic['locality'] = index['locality']
							except Exception as e:
								dic['locality'] = index['locality']
						if 'address' in index:
							dic['address'] = index['address']
						else:
							dic['address'] = ''
						if 'address_type' in index:
							dic['address_type'] = index['address_type']
						else:
							dic['address_type'] = ''
						q_dict['address'].append(dic)
				chk_health = healthCheck(q_dict)
				q_dict["chkhealth"] = chk_health
				cust_score = scoreCheck(q_dict)
				q_dict["cust_score"] = cust_score
				q_dict["since"] = record[0].created_at.strftime("%d/%b/%Y %I:%M %p")
				aa = Order.objects.filter(Company_id=q_dict["company_id"],users_id=record[0].id)
				if aa.count() > 0:
					q_dict["customer_order"] = aa.count()
					order_pattern = order_analysis(q_dict)
				else:
					q_dict["order_pattern"] = "N/A"
					q_dict["customer_order"] = 0
					order_pattern = q_dict
				final_result.append(order_pattern)
			return Response({
						"success": True, 
						"message": "Order analysis as per customer retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Order analysis as per customer retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})