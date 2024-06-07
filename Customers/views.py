from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *

#Serializer for api
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from Customers.models import CustomerProfile
from Outlet.models import OutletProfile
from Orders.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
import math  
from ZapioApi.Api.paginate import pagination
from django.db.models import Sum,Count,Max
from datetime import datetime, timedelta
from django.db.models import Q
from Configuration.models import *

from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerProfile
		fields = '__all__'

class UserlistingSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		representation = super(UserlistingSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%Y-%b-%d")
		return representation

	class Meta:
		model = CustomerProfile
		fields = '__all__'

class Userlisting(ListAPIView):
	"""
	User listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of User data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = UserlistingSerializer
	def get_queryset(self):
		user = self.request.user
		queryset = CustomerProfile.objects.all().order_by('-created_at')
		return queryset.filter(company__auth_user=user.id)


class ActiveCustomer(ListAPIView):
	"""
	User listing GET API
	
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Active user within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = UserlistingSerializer
	def get_queryset(self):
		user = self.request.user
		queryset = CustomerProfile.objects.filter(active_status=1).order_by('-created_at')
		return queryset.filter(company__auth_user=user.id)

class CustomerAction(APIView):
	"""
	Customer Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Customer account.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Customer is deactivated now!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Customer Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = CustomerProfile.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = gettext_lazy("Customer is activated successfully!!")
				else:
					info_msg = gettext_lazy("Customer is deactivated successfully!!")
				serializer = \
				CustomerSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "Customer id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Customer action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})






def order_analysis(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],users_id=q["id"])
	first_order = record[0].order_time
	last_order = record.last().order_time
	q["first_order"] = first_order.strftime("%Y-%b-%d %I:%M %p")
	q["last_order"] = last_order.strftime("%Y-%b-%d %I:%M %p")
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
	Order.objects.filter(Company_id=q["company_id"],users_id=q['id'])
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
	
	# print("ttttttttttttttttttttttttttttttt",d)

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
	Order.objects.filter(Company_id=q["company_id"],users_id=q['id'])
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
				q_dict["first_name"] = record[0].first_name
				q_dict["last_name"] = record[0].last_name
				q_dict["email"] = record[0].email
				q_dict["mobile"] = record[0].mobile
				q_dict["address"] = []
				if record[0].address1 != None:
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
				q_dict["since"] = record[0].created_at.strftime("%Y-%b-%d %I:%M %p")
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
		h_dict["order_time"] = t.strftime("%Y-%b-%d %I:%M %p")
		if i.delivery_time == None:
			h_dict["delivery_time"] = "N/A"
		else:
			d = i.delivery_time+timedelta(hours=5,minutes=30)
			h_dict["delivery_time"] = d.strftime("%Y-%b-%d %I:%M %p")
		h_dict["order_status"] = i.order_status.Order_staus_name
		#h_dict["payment_mode"] = 
		h_dict['color_code'] = i.order_status.color_code
		#h_dict['source'] = 
		q["order_history"].append(h_dict)
	return q



def order_history(q):
	record = \
	Order.objects.filter(Company_id=q["company_id"],users_id=q['id'])
	
	if record.count() > 0:
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
				r_list["created_at"] = j.created_at.strftime("%Y-%b-%d %I:%M %p")
				h_dict["log"].append(r_list)
			h_dict["order_id"] = i.outlet_order_id
			if i.is_order_now == 0:
				h_dict["order_type"] = 'Schedule Order'
				schedule_time = i.schedule_delivery_time+timedelta(hours=5,minutes=30)
				h_dict["schedule_date"] = schedule_time.strftime("%Y-%b-%d %I:%M %p")
			else:
				h_dict["order_type"] = 'Now'
				h_dict["schedule_date"] = ''
			h_dict["special_instructions"] = i.special_instructions
			t = i.order_time+timedelta(hours=5,minutes=30)
			h_dict["order_time"] = t.strftime("%Y-%b-%d %I:%M %p")

			if i.delivery_time == None or i.delivery_time == '':
				h_dict["delivery_time"] = "N/A"
			else:
				d = i.delivery_time+timedelta(hours=5,minutes=30)
				h_dict["delivery_time"] = d.strftime("%Y-%b-%d %I:%M %p")
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
		h_dict["order_time"] = i.created_on.strftime("%Y-%b-%d %I:%M %p")
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
				q_dict["first_name"] = record[0].first_name
				q_dict["last_name"] = record[0].last_name
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
				q_dict["first_name"] = i.first_name
				q_dict["last_name"] = i.last_name
				q_dict["email"] = i.email
				q_dict["mobile"] = i.mobile
				q_dict['created_at'] = i.created_at.strftime("%Y-%b-%d")
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


