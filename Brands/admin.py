from django.contrib import admin
from Brands.models import *
from datetime import datetime
from django.contrib.admin import site
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.models import User
from Configuration.admin import make_active, make_deactive
from Configuration.models import (
								PaymentDetails,
								ColorSetting,
								DeliverySetting, 
								AnalyticsSetting,
								OrderSource,
								Unit,
								PaymentMethod)
import requests
import json
# from AdroitInventry.admin_validation import CompanyForm
from UserRole.models import *
from rest_framework import serializers
from django.db.models import Q


class PermissionSerializers(serializers.ModelSerializer):
	class Meta:
		model = RollPermission
		fields = '__all__'

class BillPermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = BillRollPermission
		fields = '__all__'

def user_create(username, password,email):
	user_creation = User.objects.create_user(
						username=email,
						password=password,
						email = email,
						is_staff=False,
						is_active=True
						)

	return user_creation
	
def permissionSave(cid):
	data = {}
	userdata = UserType.objects.filter(Q(active_status=1)).order_by('id')
	for i in userdata:
		user_type = i.id
		allmenu = MainRoutingModule.objects.filter(active_status=1)
		for j in allmenu:
			main_module = j.id
			data['user_type']  = user_type
			data['main_route'] = main_module
			data['company'] = cid
			data['label'] = 1
			roll_count = RollPermission.objects.filter(Q(company=cid),Q(user_type_id=user_type),Q(main_route_id=main_module))
			if roll_count.count() > 0:
				per_serializer = PermissionSerializers(roll_count[0],data=data,partial=True)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
			else:
				per_serializer = PermissionSerializers(data=data)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
				else:
					print("aaaaaaaa",per_serializer.errors)
	return cid;

def billpermissionSave(cid):
	data = {}
	userdata = UserType.objects.filter(Q(active_status=1)).order_by('id')
	for i in userdata:
		user_type = i.id
		allmenu = BillingMainRoutingModule.objects.filter(active_status=1)
		for j in allmenu:
			main_module = j.id
			data['user_type']  = user_type
			data['main_route'] = main_module
			data['company'] = cid
			data['label'] = 1
			roll_count = BillRollPermission.objects.filter(Q(company=cid),Q(user_type_id=user_type),Q(main_route_id=main_module))
			if roll_count.count() > 0:
				per_serializer = BillPermissionSerializer(roll_count[0],data=data,partial=True)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
			else:
				per_serializer = BillPermissionSerializer(data=data)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
				else:
					print("aaaaaaaa",per_serializer.errors)
	return cid;


class CompanyAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status',

			]
#	list_display_links=None #Disable editing links

	search_fields = [
		'company_name',
		]
	list_display = [
		  'company_name',
		  'username',
		  'is_open',
		  'address',
		  'subdomain',
		  'country',
		  'state',
		  'city',
		  'logo',
		  'banner',
		'facebook',
		'instagram',
		'twitter',
		  'active_status',
		  'created_at',
		  'updated_at',
			]
	fieldsets = (
	  ('Company Details', {
		  'classes': ('wide', 'extrapretty'),
		  'fields': (
				'company_name',
				'plan_name',
				'username',
				'password',
				'business_nature',
				'company_logo',
				'subdomain',
				'company_landing_imge',
				'website',
				'attendance_type',
				'api_key',
				'eion_brand_id'
				)
	  }),
	  ('Address Details', {
		  # 'classes': ('wide',),
		  'fields': (
				'address',
				'country',
				'state',
				'city',
				'zipcode'
				)
	  }),
	  ('Statutory Details', {
		  # 'classes': ('wide',),
		  'fields': (
				'company_registrationNo',
				'company_tinnNo',
				'company_vatNo',
				'company_gstNo'
				)
	  }),
	  ('Contact Details', {
		  'classes': ('wide',),
		  'fields': (
				'company_contact_no',
				'company_email_id',
				'contact_person',
				'contact_person_mobileno',
				'contact_person_email_id',
				'contact_person_landlineno',
				'facebook',
				'instagram',
				'twitter'
				)
	  }),
	  ('Support Details', {
		  'classes': ('wide',),
		  'fields': (
					'support_person',
					'support_person_mobileno',
					'support_person_email_id',
					'support_person_landlineno'
					),
	  }),
	  ('Owner Details', {
		  'classes': ('wide',),
		  'fields': (
					'owner_name',
					'owner_email',
					'owner_phone'
					),
	  }),
	  ('Billing Details', {
		  'classes': ('wide',),
		  'fields': (
				'billing_address',
				'billing_country',
				'billing_state',
				'billing_city',
				# 'billing_currency'
				),
	  }),

	  
	)
	actions = [make_active, make_deactive]
	list_per_page = 10
	def save_model(self, request, obj, form, change):
		if not change:
			created = user_create(obj.username, obj.password,obj.company_email_id)
			user_id = User.objects.get(id=created.id)
			obj.auth_user = user_id
			obj.save()
			c_data = Company.objects.filter(auth_user=user_id.id)
			cid = c_data[0].id
			pdata = permissionSave(cid)
			bdata = billpermissionSave(cid)
			paymentdetails = PaymentDetails(company_id=cid)
			paymentdetails.save()
			themedetails = ColorSetting(company_id=cid)
			themedetails.save()
			deliverydetails = DeliverySetting(company_id=cid)
			deliverydetails.save()
			analyticsdetails = AnalyticsSetting(company_id=cid)
			analyticsdetails.save()
			order_source = add_ordersource(cid)
			unit_data = add_unit(cid)
			page_data = add_page(cid)
			tax_data = add_tax(cid)
			payment_data = add_Payment(cid)
		else:
			order_source = add_ordersource(obj.id)
			unit_data = add_unit(obj.id)
			page_data = add_page(obj.id)
			tax_data = add_tax(obj.id)
			payment_data = add_Payment(obj.id)
			if obj.subdomain:
				new_domain = add_subdomain(obj.subdomain)
				if new_domain:
					obj.website = new_domain
			auth_user = User.objects.filter(id = obj.auth_user_id)
			auth_user.update(username=obj.username)
			for user in auth_user:
				user.set_password(obj.password)
				user.save()
			obj.updated_at = datetime.now()
			obj.save()

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return True

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
	


def add_subdomain(subdomain):
	headers_cname = {
		"Authorization": "sso-key 9u52G49sfZr_9wEiVSu1Tye8G5SDjpc8jA:9UDYrAB4EHy8mDg6HC8Qai",
		'Content-Type': 'application/json'
	}
	data = [
		{
			"data": "aizo-ordering.netlify.app",
			"name": str(subdomain),
			"ttl": 3600,
			"type": "CNAME",
			"weight": 0
		}
	]
	data = json.dumps(data)
	response_cname = requests.patch("https://api.godaddy.com/v1/domains/aizotec.com/records",
									data=data, headers=headers_cname)
	print(response_cname.status_code)
	if response_cname.status_code==200:
		headers_netlify = {
			"Authorization": "Bearer 32p3CiltgAIZGkjpWX375MNiWlltZv7uUPdPnocYuns",
			'Content-Type': 'application/json'
		}
		response = requests.get("https://api.netlify.com/api/v1/sites/10243ad7-e925-475d-a2ef-89bad81480b0",
								headers=headers_netlify)
		aliases = json.loads(response.text)["domain_aliases"]
		if str(subdomain)+".aizotec.com" not in aliases:
			aliases.append(str(subdomain)+".aizotec.com")

		data = {"name":"aizo-ordering", "domain_aliases":aliases}
		data = json.dumps(data)
		response_netlify = requests.put("https://api.netlify.com/api/v1/sites/10243ad7-e925-475d-a2ef-89bad81480b0",
								data=data, headers=headers_netlify)

		print("response------", response_netlify.status_code, aliases)
		if response_netlify.status_code==200:
			return str(subdomain)+".aizotec.com"
	return None
admin.site.register(Company,CompanyAdmin)


class MergeBrandAdmin(admin.ModelAdmin):
	list_display=[
				'name',
				'get_brand',
				'active_status',
				'created_at', 
				'updated_at',
				]


admin.site.register(MergeBrand,MergeBrandAdmin)
# admin.site.register(LinkedAccount)

# admin.site.register(RouteTrack)

