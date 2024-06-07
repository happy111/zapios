import re
import json
import datetime
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.Validation.outlet_error_check import *
from _thread import start_new_thread
from django.db.models import Avg, Max, Min, Sum
from rest_framework import serializers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Brands.models import Company,Page
from UserRole.models import *
from django.db.models import Q
from rest_framework.generics import ListAPIView
from Configuration.models import *	
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from _thread import start_new_thread
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class BusinessTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = BusinessType
		fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = '__all__'
class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = RollPermission
		fields = '__all__'

class BillPermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = BillRollPermission
		fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
	class Meta:
		model = CountryMaster
		fields = '__all__'

def get_random_string(length):
	import random
	sample_letters = 'abcdefghi123456789ijklmnopqrdtyhbvgf'
	result_str = ''.join((random.choice(sample_letters) for i in range(length)))
	return result_str

def add_Payment(id):
	country_id = Company.objects.filter(id=id)[0].country_id
	payment_data = Independent_PaymentMethods.objects.filter(active_status=1)
	if payment_data.count() > 0:
		for index in payment_data:
			udata = PaymentMethod.objects.filter(payment_id=index.id,company_id=id)
			if udata.count() > 0:
				payment_method = index.payment_method
				udata.update(payment_method=payment_method,\
						payment_id=index.id,company_id=id,country_id=country_id,active_status=1)
			else:
				payment_method = index.payment_method
				sdata = PaymentMethod.objects.create(payment_method=payment_method,\
						payment_id=index.id,company_id=id,country_id=country_id,active_status=1)
		return True
	else:
		pass

def add_unit(id):
	unit_data = Independent_Unit.objects.filter(active_status=1)
	if unit_data.count() > 0:
		for index in unit_data:
			udata = Unit.objects.filter(unit_id=index.id,company_id=id)
			if udata.count() > 0:
				unit_name = index.unit_name
				short_name = index.short_name
				udata.update(unit_name=unit_name,\
						short_name=short_name,unit_id=index.id,company_id=id)
			else:
				unit_name = index.unit_name
				short_name = index.short_name
				sdata = Unit.objects.create(unit_name=unit_name,\
						short_name=short_name,unit_id=index.id,company_id=id)
		return True
	else:
		pass

def add_page(id):
	page_data = Independent_Page.objects.filter(active_status=1)
	if page_data.count() > 0:
		for index in page_data:
			udata = Page.objects.filter(page_id=index.id,company_id=id)
			if udata.count() > 0:
				title = index.title
				template = index.template
				udata.update(title=title,\
						template=template,company_id=id)
			else:
				title = index.title
				template = index.template
				sdata = Page.objects.create(title=title,\
						template=template,page_id=index.id,company_id=id)
		return True
	else:
		pass


def add_tax(id):
	tax_data = Independent_Tax.objects.filter(active_status=1)
	if tax_data.count() > 0:
		for index in tax_data:
			udata = Tax.objects.filter(tax_id=index.id,company_id=id)
			if udata.count() > 0:
				tax_name = index.tax_name
				tax_percent = index.tax_percent
				udata.update(tax_name=tax_name,\
						tax_percent=tax_percent,company_id=id)
			else:
				tax_name = index.tax_name
				tax_percent = index.tax_percent
				sdata = Tax.objects.create(tax_name=tax_name,\
						tax_percent=tax_percent,tax_id=index.id,company_id=id)
		return True
	else:
		pass

def add_ordersource(id):
	order_data = Source.objects.filter(active_status=1)
	if order_data.count() > 0:
		for index in order_data:
			sdata = OrderSource.objects.filter(source_id=index.id,company_id=id)
			if sdata.count() > 0:
				source_name = index.source_name
				img = index.image
				priority = index.priority
				sdata.update(source_name=source_name,\
						image=img,source_id=index.id,company_id=id,priority=index.priority)
			else:
				source_name = index.source_name
				img = index.image
				sdata = OrderSource.objects.create(source_name=source_name,\
						image=img,source_id=index.id,company_id=id,priority=index.priority)
		return True
	else:
		pass

def Admin_email(send_data):
	try:
		send_data['country_name']=CountryMaster.objects.filter(id=send_data['country'])[0].country
		send_data['state_name']="Delhi"
		send_data['city_name']='New Delhi'
		url = "https://api.sendgrid.com/v3/mail/send"
		headers = {'Content-type': 'application/json',
			"Authorization": "Bearer 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",
		   'Accept': 'application/json'}
		data = {
			  "personalizations": [
				{
				  "to": [
					{
					  "email": 'varun@eoraa.com',
					},

				  ],
				  "dynamic_template_data": {
				  "company_name":send_data['company_name'],
				  "company_email_id":send_data['company_email_id'],
				  "company_contact_no":send_data['company_contact_no'],
				  "country_name":send_data['country_name'],
				  "state_name" : send_data['state_name'],
				  "city_name" : send_data['city_name']
				  },

				}
			  ],
			  "from": {
				"email": "umeshsamal070@gmail.com",
				"name" : "Aizo"
			  },
				"subject": "mail_subject",
				"template_id":"d-4c51813ef0db4923a125d6d87929d08e",
				"content": [{"type": "text/html", "value": "Heya!"}]
			}
		response= requests.post(url,data=json.dumps(data),headers=headers)
	except Exception as e:
		print(e)




def Verify_user(cid):
	try:
		company_data = Company.objects.filter(id=cid)[0]
		to = company_data.company_email_id
		data = {}
		data['username'] = company_data.company_email_id
		data['password'] = company_data.password
		data['brand']    = company_data.company_name
		url = "https://api.sendgrid.com/v3/mail/send"
		headers = {'Content-type': 'application/json',
			"Authorization": "Bearer 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",
		   'Accept': 'application/json'}
		data = {
			  "personalizations": [
				{
				  "to": [
					{
					  "email": to,
					},

				  ],
				  "dynamic_template_data": {
				  "company_name": data['brand'],
				  "username": data['username'],
				  "password": data['password'],
				  },

				}
			  ],
			  "from": {
				"email": "umeshsamal070@gmail.com",
				"name" : "Aizo"
			  },
				"subject": "mail_subject",
				"template_id":"d-9b0a8289305e4dbe9319873fa03f1a69",
				"content": [{"type": "text/html", "value": "Heya!"}]
			}
		response= requests.post(url,data=json.dumps(data),headers=headers)
	except Exception as e:
		print(e)



def ConfigData(brand_id):
	paymentdetails = PaymentDetails.objects.create(company_id=brand_id)
	paymentdetails.save()
	themedetails = ColorSetting(company_id=brand_id)
	themedetails.save()
	deliverydetails = DeliverySetting(company_id=brand_id)
	deliverydetails.save()
	analyticsdetails = AnalyticsSetting(company_id=brand_id)
	analyticsdetails.save()
	order_source = add_ordersource(brand_id)
	unit_data = add_unit(brand_id)
	page_data = add_page(brand_id)
	tax_data = add_tax(brand_id)
	payment_data = add_Payment(brand_id)

	data = {}
	userdata = UserType.objects.filter(Q(active_status=1)).order_by('id')
	for i in userdata:
		user_type = i.id
		allmenu = MainRoutingModule.objects.filter(active_status=1)
		for j in allmenu:
			main_module = j.id
			data['user_type']  = user_type
			data['main_route'] = main_module
			data['company'] = brand_id
			data['label'] = 1
			roll_count = RollPermission.objects.filter(Q(company=brand_id),Q(user_type_id=user_type),Q(main_route_id=main_module))
			if roll_count.count() > 0:
				per_serializer = PermissionSerializer(roll_count[0],data=data,partial=True)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
			else:
				per_serializer = PermissionSerializer(data=data)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
				else:
					print("Error",per_serializer.errors)
	userdata = UserType.objects.filter(Q(active_status=1)).order_by('id')
	for i in userdata:
		user_type = i.id
		allmenu = BillingMainRoutingModule.objects.filter(active_status=1)
		for j in allmenu:
			main_module = j.id
			data['user_type']  = user_type
			data['main_route'] = main_module
			data['company'] = brand_id
			data['label'] = 1
			roll_count = BillRollPermission.objects.filter(Q(company=brand_id),Q(user_type_id=user_type),Q(main_route_id=main_module))
			if roll_count.count() > 0:
				per_serializer = BillPermissionSerializer(roll_count[0],data=data,partial=True)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
			else:
				per_serializer = BillPermissionSerializer(data=data)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
				else:
					print("Error",per_serializer.errors)
	return 'yes'



def User_email(to_email, mail_subject,confirmation_context, emailer_page,company_name):
	try:
		url = "https://api.sendgrid.com/v3/mail/send"
		headers = {'Content-type': 'application/json',
			"Authorization": "Bearer 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",
		   'Accept': 'application/json'}
		data = {
			  "personalizations": [
				{
				  "to": [
					{
					  "email": to_email,
					},

				  ],
				  "dynamic_template_data": {
				  "items1":confirmation_context,
				  "link": confirmation_context['reset_link'],
				  "company_name":company_name
				  },

				}
			  ],
			  "from": {
				"email": "umeshsamal070@gmail.com",
				"name" : "Aizo"
			  },
				"subject": mail_subject,
				"template_id":"d-47f08eeae5f84838a89d638e2f2e6e7c",
				"content": [{"type": "text/html", "value": "Heya!"}]
			}
		response= requests.post(url,data=json.dumps(data),headers=headers)
		if response:
			token_creation_time =  datetime.datetime.now()
			token_url = confirmation_context['reset_link']
			link_expire_create = TokenExpire.objects.create(url=token_url,\
									token_creation_time=token_creation_time)
	except Exception as e:
		print(e)



class BrandCreation(APIView):
	"""
	Brand Creation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new brand.

		Data Post: {
				"company_name"        : "QWER",
				"business_nature"     : "1",
				"username"            : "happy",
				"password"            : "12345",
				"company_email_id"    : "abc@gmail.com",
				"company_contact_no"  : "8750477293",
				"subdomain"           : "abc",
				"country"             :     "1",
				"state"               :      "1",
				"subscription_id"     : "1",
				"company_logo"        : ,
				"has_locality"		  : 1
		}

		Response: {

			"success": True,
			"message": "Outlet is registered successfully under your brand!!"
		}

	"""

	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			err_message["company_name"] = only_required(data["company_name"],"Company Name")
			err_message["business_nature"] = only_required(data["business_nature"],"Business Nature")
			err_message["company_email_id"] = \
					validation_master_anything(data["company_email_id"],
					"Company Email",email_re, 3)
			err_message["company_contact_no"] = \
					validation_master_exact(data["company_contact_no"], "Company Contact number.",contact_re, 10)
			err_message["country"] = only_required(data["country"],"Country")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			company_data = Company.objects.filter()
			data['username'] = data['company_name'].split(' ')[0] + str(000) + str(company_data.count())
			pwo = get_random_string(8)
			data['password'] =   str(pwo)
			data['password'] =   str(pwo)
			user_already_exist = User.objects.filter(username=data['username'])
			if user_already_exist.count() == 1:
				return Response(
					{
						"success": False,
						"message": "Username already exists!!"
					 }
				)
			brand_name_check = \
			Company.objects.filter(company_name__iexact=data["company_name"])
			if brand_name_check.count() == 1:
				err_message = {}
				err_message["Brandname"] = \
				"Brand with this name already exists..Please try other!!"
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
			if 'id' in data:
				pass
			else:
				create_user = User.objects.create_user(
							username=data['username'],
							password=data['password'],
							email = data['company_email_id'],
							is_staff=False,
							is_active=True
							)
				if create_user:
					data["active_status"] = 0
					data["auth_user"] = create_user.id
					data["plan_name"] = 1
					brand_serializer = BrandSerializer(data=data)
					if brand_serializer.is_valid():
						data_info = brand_serializer.save()
						brand_id = data_info.id
						current_site = get_current_site(request)
						domain = current_site.domain
						uid = urlsafe_base64_encode(force_bytes(brand_id, encoding='utf-8'))
						s = str(uid).replace('b','')
						sp = s[1:]
						spp = sp[:-1]
						confirmation_context = \
							{'user': data['company_name'],
							'reset_link': 'https://aizotec.netlify.app/confirmation/'+str(spp)}
						mail_subject = "Email Verify"
						emailer_page = 'email_templates/verify-emailer.html'
						to_email = data['company_email_id']
						reset_mail = start_new_thread(User_email,(to_email, mail_subject, \
							confirmation_context, emailer_page,data['company_name']))
						start_new_thread(Admin_email, (data,))
						config_data = start_new_thread(ConfigData,(brand_id,))
						return Response(
									{
							"success": True,
							"message": "Brand is registered successfully!!"
									}
									)
					else:
						create_user.delete()
						print(str(brand_serializer.errors))
						return Response(
						{
						"success": False, "message": str(brand_serializer.errors)
							}
							)
				else:
					create_user.delete()
					return Response(
					{
					"success": False,
					"message": "Some error occured in the process of brand manager creation!!"
					}
					)
		except Exception as e:
			print("Brand Creation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class BusinessType(ListAPIView):
	"""
	Business Type Listing GET API

		Service Usage and Description : This API is used to list all Business Type.
		Authentication Required : No
	"""

	serializer_class = BusinessTypeSerializer
	queryset = BusinessType.objects.all()



class CountryList(ListAPIView):
	"""
	Business Type Listing GET API

		Service Usage and Description : This API is used to list all Business Type.
		Authentication Required : No
	"""

	serializer_class = CountrySerializer
	queryset = CountryMaster.objects.all()


class StateList(APIView):

	"""
	All state  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to listing state via country.
		Data Post: {
			"country"		               : 1,
		}

		Response: {

			"success"		: True, 
			"message"       : "Listing state api worked well!!",
			"data"          : final_result
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			allstate = StateMaster.objects.filter(country_id=data['country'])
			final_result = []
			if allstate.count() > 0:
				for i in allstate:
					dict_source = {}
					dict_source['state'] = i.state
					dict_source['id'] = i.id
					dict_source['active_status'] = i.active_status
					final_result.append(dict_source)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("State listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class CityList(APIView):

	"""
	All city  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to listing city via state.
		Data Post: {
			"state"		               : 1,
		}

		Response: {

			"success"		: True, 
			"message"       : "Listing city api worked well!!",
			"data"          : final_result
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			allstate = CityMaster.objects.filter(state_id=data['state']).distinct('city')
			final_result = []
			if allstate.count() > 0:
				for i in allstate:
					dict_source = {}
					dict_source['city'] = i.city
					dict_source['id'] = i.id
					dict_source['active_status'] = i.active_status
					final_result.append(dict_source)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("City listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class BrandActive(APIView):

	"""
	Update Company status  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to update company status.
		Data Post: {
			"id"		               : 1,
		}

		Response: {

			"success"		: True, 

		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			cdata = Company.objects.filter(id=data['id'])
			if cdata[0].active_status == 1:
				return Response({
					"success": False, 
					"message": "Company status is updated successfully!!"})
			else:
				cdata.update(active_status=1)
				start_new_thread(Verify_user, (data['id'],))
			return Response({
					"success": True, 
					"message": "Company status is updated successfully!!"})
		except Exception as e:
			print("Company status exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})