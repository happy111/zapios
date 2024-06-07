import os,re,json,base64,time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework import serializers
from Product.models import Menu
import pyqrcode as df



class MenuSerializer(serializers.ModelSerializer):
	class Meta:
		model = Menu
		fields = '__all__'

def MenuUpload(data,menu_record,data_info):
	images_path = '/home/zapioV2/zapio/media/'
	os.remove(images_path+str(data['old_image']))
	s = os.rename(images_path+str(data_info.menu_image),images_path+str(data['old_image']))
	menu_record.update(menu_image=data['old_image'])
	return 'success'

class MenuCreationUpdation(APIView):

	"""
	Order Source Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Order Source
		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"menu_name"		           : "dddddd",
			"menu_image"					   : ""
		}

		Response: {

			"success": True, 
			"message": "Order Source creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['company'] = cid
			err_message = {}
			err_message["menu_name"] = only_required(data["menu_name"],"Menu Name")
			if type(data["menu_image"]) != str:
				im_name_path =  data["menu_image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 10000*1024:
					err_message["image_size"] = "Menu PDF can'nt excced the size more than 10000kb!!"
				filename = im_name_path
				if filename.endswith('.pdf'):
					pass
				else:
				 	err_message['ext_error'] = "Only pdf file allow!!"
			else:
				err_message['menu_image'] = "Please Upload File!!"

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = Menu.objects.filter(~Q(id=data["id"]),\
								Q(menu_name=data["menu_name"]),Q(company_id=cid))
			else:
				unique_check = Menu.objects.filter(Q(menu_name=data["menu_name"]),Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Menu Name with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			if "id" in data:
				menu_record = Menu.objects.filter(id=data['id'])
				if menu_record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Menu data is not valid to update!!"
					}
					)
				else:
					if data["menu_image"] == None:
						data["menu_image"] = menu_record[0].menu_image
					else:
						pass
					data["updated_at"] = datetime.now()
					menu_serializer = MenuSerializer(menu_record[0],data=data,partial=True)
					if menu_serializer.is_valid():
						data_info = menu_serializer.save()
						if data_info:
							time.sleep(2.4)
							menu = MenuUpload(data,menu_record,data_info)
							if menu == 'success':
								info_msg = "Menu Name is updated successfully!!"
								return Response({
									"success": True, 
									"message": info_msg
								})
					else:
						print("something went wrong!!",menu_serializer.errors)
						return Response({
							"success": False, 
							"message": str(menu_serializer.errors),
							})
			else:
				menu_serializer = MenuSerializer(data=data)
				if menu_serializer.is_valid():
					data_info = menu_serializer.save()
					menu_image = data_info.menu_image
					domain_name = addr_set()
					full_path = domain_name + str(menu_image)
					m_data = Menu.objects.filter(id=data_info.id)
					a = df.create(full_path)
					images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'../media/barcode/')
					a.png(images_path+str(data_info.id)+'.png',scale=6,module_color=[0, 0, 0, 128],
						background=[0xff, 0xff, 0xcc])
					path = '/home/zapioV2/zapio/media/barcode/'
					data_barcode = {}
					data_barcode['barcode_pic'] = str(data_info.id)+'.png'
					fpath = path + str(data_barcode['barcode_pic'])
					with open(fpath, "rb") as img_file:
						my_string = str(base64.b64encode(img_file.read()))
					slen = len(my_string)-1
					s = my_string[2:slen]
					fmstring = str('data:image/png;base64,')+str(s)
					data_barcode['barcode_info'] = full_path
					data_barcode['base_code'] = fmstring
					device_serializer = MenuSerializer(m_data[0],data=data_barcode,partial=True)
					if device_serializer.is_valid():
						customer_data_save = device_serializer.save()
					info_msg = "Menu name is created successfully!!"
				else:
					print("something went wrong!!",menu_serializer.errors)
					return Response({
						"success": False, 
						"message": str(menu_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Menu name creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})