import re,json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from rest_framework import serializers
from Configuration.models import PaymentDetails
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from .serializers import *
from Configuration.models import *
from django.db.models import Q
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy
import pandas as pd
import csv

class PaymentConfig(APIView):
	
	"""
	Percent Combo retrieval POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for payment Configuration.

		Data Post: {
			
		}

		Response: {
				"success": true,
				"keyid": "rzp_live_xcgVtA1lIkJ",
				"keySecret": "dgwbqAGqDcFXNRBYkXaP",
				"symbol": "INR"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			user = self.request.user.id
			Company_id = get_user(user)
			record = PaymentDetails.objects.filter(company=Company_id)
			if record.count() > 0:
				return Response({
							"success"   : True, 
							"id"        : record[0].id,
							"keyid" 	: record[0].keyid,
							"keySecret"	: record[0].keySecret,
							"symbol"    : record[0].symbol,
							"active_status" : record[0].active_status
							})
			else:
				return Response({
							"success": False, 
							"message": "No Data Found"
							})
		except Exception as e:
			print("Payment Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})



class PaymentEdit(APIView):
	"""
	Percent Combo retrieval POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for edit the payment Configuration.

		Data Post: {
			"keyid"                : "rzp_live_xcgVtA1lIkJ",
			"keySecret"            : "dgwbqAGqDcFXNRBYkXaP",
			"symbol"			   : "INR"
			"id"                   : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Percent Combo retrieval api worked well!!",
			"data"     : final_result
		}

	"""
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			record = PaymentDetails.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
					{
						"status": False,
						"message": gettext_lazy("Payment Configuration data is not valid to update!!")
					})
			else:
				data["updated_at"] = datetime.now()
				payment_serializer = \
					PaymentSerializer(record[0],data=data,partial=True)
				if payment_serializer.is_valid():
					data_info = payment_serializer.save()
					return Response({
						"status": True, 
						"message": gettext_lazy("Payment credentials are updated successfully!!"),
						"data": payment_serializer.data
						})
				else:
					print("something went wrong!!")
					return Response({
						"status": False, 
						"message": str(payment_serializer.errors),
						})
		except Exception as e:
			print("Payment Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})


class PaymentAction(APIView):
	"""
	Payment Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Payment Configuration.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Payment Configuration is deactivated now!!",
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
				err_message["active_status"] = gettext_lazy("Active status data is not valid!!")
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Payment Configuration Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = PaymentDetails.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = gettext_lazy("Payment Configuration is activated successfully!!")
				else:
					info_msg = gettext_lazy("Payment Configuration is deactivated successfully!!")
				serializer = \
				PaymentSerializer(record[0],data=data,partial=True)
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
						"message": gettext_lazy("Payment Configuration id is not valid to update!!")
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
			print("Payment Configuration action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class PaymentRetrieve(APIView):
	"""
	Percent Combo retrieval POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieve the payment Configuration.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Percent Combo retrieval api worked well!!",
			"data"     : final_result
		}

	"""
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			record = PaymentDetails.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
					{
						"status": False,
						"message": gettext_lazy("Payment Configuration data is not valid to update!!")
					})
			else:
				payment_serializer = PaymentSerializer(record, many=True)
				return Response({
						"status": True, 
						"message": gettext_lazy("Payment Configuration data updation api worked well!!"),
						"data": payment_serializer.data
						})
		except Exception as e:
			print("Payment Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})



class ActiveTaxlisting(APIView):
	"""
	Active Tax listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of active Taxes brandwise.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			record = TaxSetting.objects.filter(active_status=1,company=cid)
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": gettext_lazy("Required data is not found!!")
				}
				)
			else:
				final_result = []
				for q in record:
					q_dict = {}
					q_dict["id"] =  q.id
					q_dict["taxs"] =  q.tax_name
					q_dict["tax_name"] = \
					str(q.tax_name)+" | "+str(q.tax_percent)+"%" 
					final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": gettext_lazy("Active tax data listing api worked well!!"),
						"data": final_result,
						})
		except Exception as e:
			print("Active tax data listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class DeliveryConfig(APIView):
	
	"""
	Delivery & Packaging Config GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for delivery & Packaging charge Configuration details.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			user = self.request.user.id
			auth_id = user
			Company_id = get_user(auth_id)
			record = DeliverySetting.objects.filter(company=Company_id)
			Final_result = []
			if record.count() > 0:
				price_type  = record[0].price_type
				q_dict = {}
				q_dict['price_type'] = []
				if price_type != None:
					i_dict={}
					i_dict["value"] = price_type
					i_dict["key"] = price_type
					i_dict["label"] = price_type
					q_dict["price_type"].append(i_dict)
				else:
					pass
				q_dict['is_tax'] = record[0].is_tax
				q_dict['delivery_charge'] = record[0].delivery_charge
				q_dict['package_charge'] = record[0].package_charge
				q_dict['delivery_id'] = record[0].id
				q_dict['delivery_status'] = record[0].active_status
				q_dict['tax'] = []
				ps = record[0].tax
				if ps !=None:
					for v in ps:
						pname = Tax.objects.filter(id=str(v))[0]
						dic =  {}
						dic["label"] = str(pname.tax_name)+" | "+str(pname.tax_percent)+"%" 
						dic["value"] = str(v)
						q_dict['tax'].append(dic)
				else:
					pass
			else:
				err_message = {}
				err_message["settings"] = gettext_lazy("Please contact to super-admin to set parameters for this!!")
				return Response({
							"success": False, 
							"error" :  err_message
							})
			record = PaymentDetails.objects.filter(company=Company_id)
			if record.count() > 0:
				q_dict['payment_id'] = record[0].id
				q_dict['keyid'] = record[0].keyid
				q_dict['keySecret'] = record[0].keySecret
				q_dict['symbol'] = record[0].symbol
				q_dict['payment_status'] = record[0].active_status
			else:
				pass
			record = ColorSetting.objects.filter(company=Company_id)
			if record.count() > 0:
				q_dict['theme_id'] = record[0].id
				q_dict['accent_color'] = record[0].accent_color
				q_dict['textColor'] = record[0].textColor
				q_dict['secondaryColor'] = record[0].secondaryColor
				q_dict['theme_status'] = record[0].active_status
			else:
				pass
			record = AnalyticsSetting.objects.filter(company=Company_id)
			if record.count() > 0:
				q_dict['google_id'] = record[0].id
				q_dict['u_id'] = record[0].u_id
				q_dict['analytics_snippets'] = record[0].analytics_snippets
				q_dict['google_status'] = record[0].active_status
			else:
				pass
			Final_result.append(q_dict)
			return Response({
						"success"   : True, 
						"data"      : Final_result
							})
		except Exception as e:
			print("Delivery Charge Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})




class DeliveryEdit(APIView):

	"""
	Delivery & Packaging Configuration Edit POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to edit the delivery & packaging Configuration details.

		Data Post: {
			"delivery_charge"                : "#ffd600",
			"package_charge"                 : "#000",
			"tax_percent"                     : "#ffd600",
			"CGST"                            : "#000",
			"id"                              : "1"
			product_method                     : []
		}

		Response: {

			"success"  : True, 
			"message"  : "Theme api worked well!!",
			"data"     : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from Brands.models import Company
			data = request.data
			user = request.user
			auth_id = user.id
			Company_id = get_user(auth_id)
			if data['tab'] == str(0):
				record = PaymentDetails.objects.filter(id=data['payment_id'])
				if record.count() == 0:
					return Response(
						{
							"status": False,
							"message": gettext_lazy("Payment Configuration data is not valid to update!!")
						})
				else:
					data["updated_at"] = datetime.now()
					payment_serializer = \
						PaymentSerializer(record[0],data=data,partial=True)
					if payment_serializer.is_valid():
						data_info = payment_serializer.save()
						return Response({
							"status": True, 
							"message": gettext_lazy("Payment credentials are updated successfully!!"),
							"data": payment_serializer.data
							})
					else:
						print("something went wrong!!")
						return Response({
							"status": False, 
							"message": str(payment_serializer.errors),
							})
			if data['tab'] == str(1):
				err_message = {}
				err_message["accent_color"] =  only_required(data["accent_color"],"Accent Color")
				err_message["textColor"] =  only_required(data["textColor"],"Text Color")
				err_message["secondaryColor"] =  only_required(data["secondaryColor"],"Secondary Color")
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})

				record = ColorSetting.objects.filter(Q(id=data['theme_id']),Q(company=Company_id))
				if record.count() == 0:
					return Response(
						{
							"status": False,
							"message": gettext_lazy("Theme Configuration data is not valid to update!!")
						})
				else:
					data["updated_at"] = datetime.now()
					theme_serializer = \
						ThemeSerializer(record[0],data=data,partial=True)
					if theme_serializer.is_valid():
						data_info = theme_serializer.save()
						return Response({
							"status": True, 
							"message": gettext_lazy("Theme Configuration is updated successfully!!"),
							"data": theme_serializer.data
							})
					else:
						print("something went wrong!!")
						return Response({
							"status": False, 
							"message": str(theme_serializer.errors),
							})
						

			

			if data['tab'] == str(2):
				err_message = {}
				err_message["u_id"] =  only_required(data["u_id"],"User Id")
				err_message["analytics_snippets"] =  \
				only_required(data["analytics_snippets"],"Analytics Snippet")
				err_message["id"] = validation_master_anything(str(data["google_id"]),
									"Id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				record = AnalyticsSetting.objects.filter(Q(id=data['google_id']),Q(company=Company_id))
				if record.count() == 0:
					return Response(
						{
							"status": False,
							"message": gettext_lazy("Analytics Configuration data is not valid to update!!")
						})
				else:
					data["updated_at"] = datetime.now()
					serializer = \
						AnalyticsSerializer(record[0],data=data,partial=True)
					if serializer.is_valid():
						data_info = serializer.save()
						return Response({
							"status": True, 
							"message": gettext_lazy("Google Analytics Configuration is updated successfully!!"),
							"data": serializer.data
							})
					else:
						print("something went wrong!!")
						return Response({
							"status": False, 
							"message": str(serializer.errors),
							})

		except Exception as e:
			print("Delivery Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})




class DeliveryAction(APIView):
	"""
	Payment Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Delivery & Packaging Configuration.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Delivery & Packaging Configuration setting is deactivated successfully!!",
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
			if data['tab'] == str(0):
				if data["active_status"] == "true":
					pass
				elif data["active_status"] == "false":
					pass
				else:
					err_message["active_status"] = gettext_lazy("Active status data is not valid!!")
				err_message["id"] = \
							validation_master_anything(data["id"],
							"Payment Configuration Id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				record = PaymentDetails.objects.filter(id=str(data["id"]))
				if record.count() != 0:
					data["updated_at"] = datetime.now()
					if data["active_status"] == "true":
						info_msg = gettext_lazy("Payment Configuration is activated successfully!!")
					else:
						info_msg = gettext_lazy("Payment Configuration is deactivated successfully!!")
					serializer = \
					PaymentSerializer(record[0],data=data,partial=True)
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
							"message": gettext_lazy("Payment Configuration id is not valid to update!!")
						}
						)
				final_result = []
				final_result.append(serializer.data)
				return Response({
							"success": True, 
							"message": info_msg,
							"data": final_result,
							})
			if data['tab'] == str(1):
				if data["active_status"] == "true":
					pass
				elif data["active_status"] == "false":
					pass
				else:
					err_message["active_status"] = gettext_lazy("Active status data is not valid!!")
				err_message["id"] = \
							validation_master_anything(data["id"],
							"Theme Configuration Id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				record = ColorSetting.objects.filter(id=data["id"])
				if record.count() != 0:
					data["updated_at"] = datetime.now()
					if data["active_status"] == "true":
						info_msg = gettext_lazy("Theme Configuration is activated successfully!!")
					else:
						info_msg = gettext_lazy("Theme Configuration is deactivated successfully!!")
					serializer = \
					ColorSerializer(record[0],data=data,partial=True)
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
							"message": "Theme Configuration id is not valid to update!!"
						}
						)
				final_result = []
				final_result.append(serializer.data)
				return Response({
							"success": True, 
							"message": info_msg,
							"data"   : final_result,
							})
			if data['tab'] == str(2):
				if data["active_status"] == "true":
					pass
				elif data["active_status"] == "false":
					pass
				else:
					err_message["active_status"] = gettext_lazy("Active status data is not valid!!")
				err_message["id"] = \
							validation_master_anything(data["id"],
							"Delivery setting Configuration Id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				record = DeliverySetting.objects.filter(id=data["id"])
				if record.count() != 0:
					data["updated_at"] = datetime.now()
					if data["active_status"] == "true":
						info_msg = gettext_lazy("Delivery & Packaging Configuration setting is activated successfully!!")
					else:
						info_msg = gettext_lazy("Delivery & Packaging Configuration setting is deactivated successfully!!")
					serializer = \
					ColorSerializer(record[0],data=data,partial=True)
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
							"message": "Delivery Charge Configuration id is not valid to update!!"
						}
						)
				final_result = []
				final_result.append(serializer.data)
				return Response({
							"success": True, 
							"message": info_msg,
							"data": final_result,
							})
			if data['tab'] == str(3):
				if data["active_status"] == "true":
					pass
				elif data["active_status"] == "false":
					pass
				else:
					err_message["active_status"] = "Active status data is not valid!!"
				err_message["id"] = \
							validation_master_anything(data["id"],
							"Theme Configuration Id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				record = AnalyticsSetting.objects.filter(id=data["id"])
				if record.count() != 0:
					data["updated_at"] = datetime.now()
					if data["active_status"] == "true":
						info_msg = gettext_lazy("Google Analytics Configuration setting is activated successfully!!")
					else:
						info_msg = gettext_lazy("Google Analytics Configuration setting is deactivated successfully!!")
					serializer = \
					AnalyticsSerializer(record[0],data=data,partial=True)
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
							"message": "Analytics Configuration id is not valid to update!!"
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
			print("Delivery & Packaging Configuration action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class PaymentList(APIView):
	"""
	Payment listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of payment brandwise.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			types = ['delivery','pickup']
			data_payment = OnlinepaymentStatus.objects.filter(company_id=cid)
			if data_payment.count() > 0:
				pass
			else:
				for index in types:
					payment_data = PaymentMethod.objects.filter(company_id=cid)
					if payment_data.count() > 0:
						for i in payment_data:
							if i.payment_method == 'Razorpay' or i.payment_method == 'Cash':
								status_data = OnlinepaymentStatus.objects.create(types=index,payment_id=i.id,\
									company_id=cid,is_hide=0)
							else:
								status_data = OnlinepaymentStatus.objects.create(types=index,payment_id=i.id,\
									company_id=cid,is_hide=1)
			record = OnlinepaymentStatus.objects.filter(company=cid,is_hide=0)
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Required data is not found!!"
				}
				)
			else:
				final_result = []
				for q in record:
					q_dict = {}
					q_dict["id"] =  q.id
					q_dict["types"] =  q.types
					q_dict["payment_id"] =  q.payment_id
					q_dict["payment_method"] =  q.payment.payment_method
					q_dict['active_status'] = q.active_status
					final_result.append(q_dict)
			return Response({
						"success": True, 
						"data": final_result,
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





class PaymentAction(APIView):
	"""
	Payment Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Payment.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 

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
				err_message["active_status"] = gettext_lazy("Active status data is not valid!!")
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Payment Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = OnlinepaymentStatus.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = gettext_lazy("Payment Status is activated successfully!!")
				else:
					info_msg = gettext_lazy("Payment Status is deactivated successfully!!")
				serializer = \
				ProductStatus(record[0],data=data,partial=True)
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
						"message": gettext_lazy("Payment Status is not valid to update!!")
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
			print("Payment action Api Stucked into exception!!")
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


def decode_utf8(input_iterator):
    for l in input_iterator:
        yield l.decode('utf-8')

def reg_parse(file):
    for row in csv.reader(decode_utf8(file)):
        yield row

class AutoFetch(APIView):
	"""
	Autofetch address POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to autofetch address.

		Data Post: {

		}

		Response: {

			"success": True, 

		}

	"""
	# permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			reader = csv.reader(decode_utf8(request.FILES['file']))
			next(reader, None)
			i = 1
			for row in reader:
				pd = {}
				obj_data = Address.objects.filter(pincode=row[0])
				if obj_data.count() > 0:
					print(row[0])
					# for i in obj_data:
					# 	obj_data1 = Address.objects.filter(id=i.id)
					# 	if obj_data1.count() > 1:
					# 		obj_data = Address.objects.filter(id=i.id)
					# 		obj_data.delete()
					# 		print("2")
					# 	else:
					# 		print("1")

				else:
					print("3")
					pd['pincode'] = row[0]
					pd['prefecture'] = row[1]
					pd['city'] = row[2]
					pd['address'] = row[3]
					getLoc = Address.objects.create(pincode=pd['pincode'],prefecture=pd['prefecture'] ,city=row[2],address=row[3])
					getLoc.save()
			return Response({
					"success": True, 
					})
		except Exception as e:
			return Response({
					"success": False, 
					"message" : str(e)
					})


class AutoFetchAddress(APIView):
	"""
	Autofetch address POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to autofetch address.

		Data Post: {
			pincode : "110025"
		}

		Response: {

			"success": True, 

		}

	"""
	# permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			getAddress =Address.objects.filter(pincode=data['pincode'])
			if getAddress.count() > 0:
				dataAdd = {}
				dataAdd['prefecture'] = getAddress[0].prefecture
				dataAdd['city'] = getAddress[0].city
				dataAdd['address'] = getAddress[0].address
				return Response({
						"success": True, 
						"data":dataAdd
						})
			else:
				return Response({
						"success": False,
						"message": "No data Found" 
						})
		except Exception as e:
			return Response({
					"success": False, 
					"message" : str(e)
					})

	