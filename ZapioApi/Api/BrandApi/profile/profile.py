from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Max
from Brands.models import Company

#Serializer for api
from rest_framework import serializers
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
AddonDetails
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from ZapioApi.api_packages import *



class CompanySerializer(serializers.ModelSerializer):
	
	def to_representation(self, instance):
		representation = super(CompanySerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		domain_name = addr_set()
		representation['company_logo'] = str(instance.company_logo)
		if representation['company_logo'] != "" and representation['company_logo'] != None:
			full_path = domain_name + str(instance.company_logo)

			representation['company_logo'] = full_path
		else:
			pass
		representation['company_landing_imge'] = str(instance.company_landing_imge)
		representation['api_key'] = str(instance.api_key)

		if representation['company_landing_imge'] != "" and representation['company_landing_imge'] != None:
			full_path = domain_name + str(instance.company_landing_imge)
			representation['company_landing_imge'] = full_path
		else:
			pass
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = Company
		fields = '__all__'


class ProfileUpdation(APIView):
	"""
	Company profile Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to update brand profile details.

		Data Post: {
			"company_logo"         		: "logo.jpg",
			"address"              		: "Mayur vihar phase 2",
			"website"              		: "instapizza.in",
			"support_person"       		: "Ujjwal",
			"support_person_email_id"	: "ujjwal@mail.com",
			"support_person_mobileno"   : "8787878787",
			"owner_name"                : "Ashwin",
			"owner_email"               : "ashwin@mail.com",
			"owner_phone"               : "8484848484",
			"company_landing_imge"      : "banner.jpg",
			"instagram"                  :
 			"facebook"
		}

		Response: {

			"success": True, 
			"message": "Profile is updated successfully!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			err_message = {}
			if type(data["company_logo"]) != str:
				im_name_path =  data["company_logo"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 10000*1024:
					err_message["image_size"] = "Company logo image can'nt excced the size more than 10kb!!"
			else:
				data["company_logo"] = None
			if type(data["company_landing_imge"]) != str:
				im_name_path =  data["company_landing_imge"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 5000000000000000000000*1024:
					err_message["company_landing_imge"] = \
					"Company banner image can'nt excced the size more than 500kb!!"
			else:
				data["company_landing_imge"] = None
			err_message["address"] = \
				validation_master_anything(data["address"],
					"Address",address_re, 4)
			err_message["website"] = \
				validation_master_anything(data["website"],
					"Website",web_re,3)
			err_message["support_person"] = \
				validate_anything(data["support_person"], alpha_re, 
					zero__re,3, "Support person name")
			err_message["support_person_mobileno"] = \
				validation_master_exact(data["support_person_mobileno"],
					"Support Person Mobile No.",contact_re, 10)
			err_message["support_person_email_id"] = \
				validation_master_anything(data["support_person_email_id"],
					"Support Mail Id",email_re, 3)
			err_message["owner_name"] = \
				validation_master_anything(data["owner_name"],
					"Owner Name",alpha_re, 3)
			err_message["owner_phone"] = \
				validation_master_exact(data["owner_phone"],
					"Owner Mobile No.",contact_re, 10)
			err_message["owner_email"] = \
				validation_master_anything(data["owner_email"],
					"Owner Mail Id",email_re, 3)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			user = request.user
			record = Company.objects.filter(id=Company_id)
			if data["company_logo"] == None:
				data["company_logo"] = record[0].company_logo
				if data["company_logo"] != None and data["company_logo"] != "":
					pass
				else:
					data["company_logo"] = None
			else:
				pass
			if data["company_landing_imge"] == None:
				data['company_landing_imge'] = record[0].company_landing_imge
				if data["company_landing_imge"] != None and data["company_landing_imge"] != "":
					pass
				else:
					data["company_landing_imge"] = None
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided data is not valid to update!!"
				}
				)
			else:
				data["updated_at"] = datetime.now()
				serializer = \
				CompanySerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": "Profile is updated successfully!!",
						"data": final_result,
						})
		except Exception as e:
			print("Cmpany profile updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
