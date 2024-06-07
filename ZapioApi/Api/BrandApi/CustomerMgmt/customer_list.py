from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
import json
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from Customers.models import CustomerProfile
from Orders.models import Order
from django.db.models import Sum,Count,Max
from Outlet.models import OutletProfile
from ZapioApi.Api.paginate import pagination
import math  
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Product.models import Product


def order_analysis(q):
	record = \
	Order.objects.filter(Q(Company_id=q["company_id"]),Q(users_id=int(q['id'])))
	first_order = record[0].order_time
	last_order = record.last().order_time
	q["total_order"] = record.count()
	full_addr = record.last().address
	q["address"] = full_addr
	total_spent = record.aggregate(Sum('total_bill_value'))
	q["total_spent"] = total_spent['total_bill_value__sum']
	q_pre_outlet = record.values('outlet').annotate(visit_count=Count('outlet'))
	visited_outlet = {}
	for i in q_pre_outlet:
		visited_outlet[i["outlet"]] = i["visit_count"]
	outlet_id = max(visited_outlet, key=visited_outlet.get) 
	q["preferred_outlet"] = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
	day_diff = (last_order.date()-first_order.date()).days
	print("c",q)
	return q

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

def countTag(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],users_id=q['id'])
	if record.count() > 0:
		totaltag = 0
		for index in record:
			order_description = index.order_description
			for k in order_description:
				if 'product_id' in k:
					product_data = Product.objects.filter(id=k['product_id'])
					if product_data.count() > 0:
						alltag = product_data[0].tags
						totaltag = totaltag + len(alltag)
	return totaltag


class Userlisting(APIView):
	"""
	Customer Listing / Search POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide product Listing / search.

		Data Post: {

			"search"   ; "santosh",
			"page"     :
		}

		Response: {

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = self.request.user.id
			Company_id = get_user(user)
			data = request.data
			if data['search'] != '':
				allcustomer = CustomerProfile.objects.filter(Q(company=Company_id)
				,Q(name__icontains=data['search'])|Q(mobile__icontains=data['search'])).order_by('-created_at')
			else:
				allcustomer = CustomerProfile.objects.filter(company=Company_id).order_by('-created_at')
			q_count = allcustomer.count()
			page_count = math.ceil((q_count/20))
			page = data['page']
			paged_query = pagination(allcustomer,page)
			final_result = []
			total = 0
			for i in paged_query:
				q_dict = {}
				q_dict["id"] = i.id
				q_dict["company_id"] = i.company_id
				q_dict["name"] = i.name
				q_dict["email"] = i.email
				q_dict["mobile"] = i.mobile
				q_dict['created_at'] = i.created_at.strftime("%d/%b/%y")
				aa = Order.objects.filter(Company_id=q_dict["company_id"],\
					                users_id=i.id)
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
					order_pattern = order_analysis(q_dict)
					chk_health = healthCheck(q_dict)
					q_dict["chkhealth"] = chk_health
					customer_tag = countTag(q_dict)
					q_dict["totaltag"] = customer_tag
				else:
					q_dict["total_order"] = "N/A"
					q_dict["total_spent"] = "N/A"
					order_pattern = q_dict
				final_result.append(order_pattern)


			return Response({"status":True,
							"data":final_result,
							"page_count":page_count})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


