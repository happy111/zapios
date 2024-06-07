import os
import re
import json
import requests
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_401_UNAUTHORIZED,
    HTTP_417_EXPECTATION_FAILED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Brands.models import Page,HomePage,HomepagePromotion,Company
from django.db.models import Q
from rest_framework.views import APIView
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Product.models import Menu
from History.models import MenuCounts
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from Configuration.models import *
from .serializers import *
import dateutil.parser,uuid
from Orders.models import Order
from Event.models import *
from History.models import *
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy

class CountCheckout(APIView):
	"""
	Count checkout GET API
		Authentication Required		: No
		Service Usage & Description	: This Api is used for providing count reaches checkout.
		Request param: url   (ex: url=sushijunction.aizotec.com)
		Request param: menu_id : 2
	"""
	def get(self, request, format=None):
		try:
			url =["http://" + str(request.query_params["url"]),
				  "https://" + str(request.query_params["url"]),
				  str(request.query_params["url"])]
			if url:
				data = Company.objects.filter(website__in=url)
				if data.count()!=0:
					company_data = data[0]
					c_id = company_data.id
					save_wev = WebsiteStatistic.objects.create(name=company_data.company_name,\
						checkout=1,company_id=company_data.id)
					info_msg = "User reaches checkout page Successfully!!"
					return Response({
							"success": True, 
							"message": gettext_lazy(info_msg)
						})
			else:
				return Response({
						"success": False, 
						"message": gettext_lazy("Url Not Found")
						})
		except Exception as e:
			print("checkout count Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})






class MenuCount(APIView):
	"""
	Menu Count GET API
		Authentication Required		: No
		Service Usage & Description	: This Api is used for providing count no of view.
		Request param: url   (ex: url=sushijunction.aizotec.com)
		Request param: menu_id : 2
	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			mdata = MenuCounts.objects.filter(event_time__date=datetime.now().date(),company_id=cid)
			sb_result = mdata.values('company','menu_name').\
								annotate(id=Sum('id'),menu_view=Count("menu_id"))
			final_result = []
			total = 0
			if sb_result.count() > 0:
				for index in sb_result:
					dic = {}
					dic['menu_name'] = index['menu_name']
					dic['menu_view'] = index['menu_view']
					total = total + int(index['menu_view'])
					final_result.append(dic)
			return Response({
					"success": True, 
					"data":  final_result,
					"toal_view" : total
					})
		except Exception as e:
			print("Page creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

class MenuView(APIView):
	"""
	Menu View GET API
		Authentication Required		: No
		Service Usage & Description	: This Api is used for providing count no of view.
		Request param: url   (ex: url=sushijunction.aizotec.com)
		Request param: menu_id : 2
	"""
	def get(self, request, format=None):
		try:
			url =["http://" + str(request.query_params["url"]),
				  "https://" + str(request.query_params["url"]),
				  str(request.query_params["url"])]
			if url:
				data = Company.objects.filter(website__in=url)
				if data.count()!=0:
					company_data = data[0]
					c_id = company_data.id
					c = Menu.objects.filter(id=request.query_params['menu_id'])
					if c.count() > 0:
						mname = c[0].menu_name
						data = {}
						data['company'] = c_id
						data['menu'] = request.query_params['menu_id']
						data['menu_name'] = mname
						page_serializer = MenuSerializer(data=data)
						if page_serializer.is_valid():
							data_info = page_serializer.save()
							info_msg = "Menu View Successfully!!"
							return Response({
									"success": True, 
									"message": gettext_lazy(info_msg)
								})
						else:
							return Response({
									"success": False, 
									"message": page_serializer.errors
								})
					else:
						return Response({
									"success": False, 
									"message": gettext_lazy("Menu id not found!!")
								})
			else:
				return Response({
						"success": False, 
						"message": gettext_lazy("Url Not Found")
						})
		except Exception as e:
			print("Page creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class PageCreate(CreateAPIView):
	"""
	Page Creation POST API View

		Service usage and description : This API is used to create a page.
		Authentication Required : YES

		Request Body Data :
		{
			"title" : "ABC",                                      //required
			"content" : ""                                        //required
			"template" : "abc"									  //required
		}
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = PageSerializer

	def post(self, request, *args, **kwargs):
		try:
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['company'] = cid
			err_message = {}
			err_message["title"] = only_required(data["title"],"Title")
			err_message["content"] = only_required(data["content"],"Content")
			err_message["template"] = only_required(data["template"],"Template")
			if "id" in data:
				unique_check = Page.objects.filter(~Q(id=data["id"]),\
								Q(title=data["title"]),Q(company_id=cid))
			else:
				unique_check = Page.objects.filter(Q(title=data['title']),\
										Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = gettext_lazy("Title with this name already exists!!")
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				page_record = Page.objects.filter(id=data['id'])
				if page_record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Page data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					serializer = PageSerializer(page_record[0],data=data,partial=True)
					if serializer.is_valid():
						data_info = serializer.save()
						info_msg = "Page  is updated successfully!!"
						return Response({
							"success": True, 
							"message": info_msg
						})
					else:
						print("something went wrong!!",serializer.errors)
						return Response({
							"success": False, 
							"message": str(serializer.errors),
							})
			else:
				serializer = PageSerializer(data=data)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "Page is created successfully!!"
					return Response({
							"success": True, 
							"message": info_msg
						})
				else:
					print("something went wrong!!",serializer.errors)
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
		except Exception as e:
			print("Page creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class PageListingAPI(ListAPIView):
	"""
	Page Listing GET API

		Service Usage and Description : This API is used to listing of page.
		Authentication Required : YES

		Params : {

		}
	"""

	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		user = self.request.user
		user = user.id
		cid = get_user(user)
		queryset = Page.objects.filter(company_id=cid).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = PageSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Page listing API worked well!!"})


class PageRetrieveAPI(RetrieveAPIView):
	"""
	Company(key/Door) Retrieve API View

		Service usage and description : This API is used to retrieve company info.
		Authentication Required : YES
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = PageRetrieveSerializer
	queryset = Page.objects.all()


class PageActionAPI(APIView):

	"""
	Page Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate page.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Page is deactivated now!!",
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
						"Page Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Page.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Page is activated successfully!!"
				else:
					info_msg = "Page is deactivated successfully!!"
				serializer = PageSerializer(record[0],data=data,partial=True)
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
						"message": "Page id is not valid to update!!"
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
			print("Page action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class HomeCreate(APIView):
	"""
	Home Page Creation POST API View

		Service usage and description : This API is used to create a Home page.
		Authentication Required : YES

		Request Body Data :
		{
			"web_slider"            : "image field",                                      
			"mobile_slider"         : "image field"                                       
			"carousel_text"         : "abc"	,
			"carousel_image"        : "image",
			"carousel_text1"        : "abc",
			"carousel_image1"       : "image",
			"health_text"           : "text",
			"health_image"		    : 'image',
			"promotions_image"		: "image"	 
			"is_promotions"         :
			"promotions_url"        :
		}
	"""

	permission_classes = (IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['company'] = cid
			err_message = {}
			if data['is_promotions'] == 'true':
				data['is_promotions'] = 1
			else:
				data['is_promotions'] = 0
			if type(data["web_slider"]) != str:
				im_name_path =  data["web_slider"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 1000*1024:
					err_message["image_size"] = "Web slider can'nt excced the size more than 100kb!!"
			else:
				err_message["web_slider"]  = "Please Choose Web Slider"
			if type(data["mobile_slider"]) != str:
				im_name_path =  data["mobile_slider"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 1000*1024:
					err_message["image_size"] = "Mobile mobile can'nt excced the size more than 100kb!!"
			else:
				data["mobile_slider"] = ''
			if type(data["carousel_image"]) != str:
				im_name_path =  data["carousel_image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 1000*1024:
					err_message["image_size"] = "Carousel image mobile can'nt excced the size more than 100kb!!"
			else:
				data["carousel_image"] = ''
			if type(data["carousel_image1"]) != str:
				im_name_path =  data["carousel_image1"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 1000*1024:
					err_message["image_size"] = "Carousel image1 mobile can'nt excced the size more than 100kb!!"
			else:
				data["carousel_image1"] = ''

			if type(data["health_image"]) != str:
				im_name_path =  data["health_image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 1000*1024:
					err_message["image_size"] = "Health image can'nt excced the size more than 100kb!!"
			else:
				data["health_image"] = ''
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			homedata = HomePage.objects.filter(company_id=cid)
			if homedata.count() > 0:
				p_query = homedata.update(
					carousel_text=data['carousel_text'],\
					carousel_text1=data['carousel_text1'],\
					health_text=data['health_text'],\
					is_promotions=data['is_promotions'],\
					promotions_url=data['promotions_url'])
				if data["web_slider"] != None and data["web_slider"] != "":
					product = HomePage.objects.get(id=homedata[0].id)
					product.web_slider = data["web_slider"]
					product.save()
				else:
					pass
				if data["mobile_slider"] != None and data["mobile_slider"] != "":
					product = HomePage.objects.get(id=homedata[0].id)
					product.mobile_slider = data["mobile_slider"]
					product.save()
				else:
					pass
				if data["carousel_image"] != None and data["carousel_image"] != "":
					product = HomePage.objects.get(id=homedata[0].id)
					product.carousel_image = data["carousel_image"]
					product.save()
				else:
					pass

				if data["carousel_image1"] != None and data["carousel_image1"] != "":
					product = HomePage.objects.get(id=homedata[0].id)
					product.carousel_image1 = data["carousel_image1"]
					product.save()
				else:
					pass

				if data["health_image"] != None and data["health_image"] != "":
					product = HomePage.objects.get(id=homedata[0].id)
					product.health_image = data["health_image"]
					product.save()
				else:
					pass
				if "image0" not in data and "image1" not in data and "image2" not in data \
					and "image3" not in data:
					pass
				else:
					i_query = HomepagePromotion.objects.filter(homepage_id=homedata[0].id)
					i_query.delete()
					if "image0" in data:
						i_query = HomepagePromotion.objects.create(promotions_image=data['image0'],\
									homepage_id=homedata[0].id)
					if "image1" in data:
						i_query = HomepagePromotion.objects.create(promotions_image=data['image1'],\
									homepage_id=homedata[0].id)
					if "image2" in data:
						i_query = HomepagePromotion.objects.create(promotions_image=data['image2'],\
									homepage_id=homedata[0].id)
					if "image3" in data:
						i_query = HomepagePromotion.objects.create(promotions_image=data['image3'],\
									homepage_id=homedata[0].id)
				if p_query:
					data_info = p_query
					info_msg = "Home page is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": "Error",
						})
			else:

				p_query = HomePage.objects.create(company_id=cid,home='Home',web_slider=data['web_slider'],\
					mobile_slider=data['mobile_slider'],carousel_text=data['carousel_text'],\
					carousel_image=data['carousel_image'],carousel_text1=data['carousel_text1'],\
					carousel_image1=data['carousel_image1'],health_text=data['health_text'],\
					health_image=data['health_image'],is_promotions=data['is_promotions'],\
					promotions_url=data['promotions_url'])

				if "image0" in data:
					i_query = HomepagePromotion.objects.create(promotions_image=data['image0'],\
						homepage_id=p_query.id)
				if "image1" in data:
					i_query = HomepagePromotion.objects.create(promotions_image=data['image1'],\
						homepage_id=p_query.id)
				if "image2" in data:
					i_query = HomepagePromotion.objects.create(promotions_image=data['image2'],\
						homepage_id=p_query.id)
				if "image3" in data:
					i_query = HomepagePromotion.objects.create(promotions_image=data['image3'],\
						homepage_id=p_query.id)
				if p_query:
					data_info = p_query
					p_id = data_info.id
					info_msg = "Home page is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": "Error",
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Home Page creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class HomeRetrieveAPI(APIView):

	"""
	Home Page Retrieve POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to retrieve home page.

		Data Post: {
			"company_id"                   		: "2",

		}

		Response: {

			"success": True, 
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
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			final_result = []
			record = HomePage.objects.filter(company_id=Company_id)
			if record.count() != 0:
				dic = {}
				domain_name = addr_set()
				if record[0].web_slider != None:
					dic['web_slider'] = domain_name + str(record[0].web_slider)
				else:
					dic['web_slider'] = ''

				if record[0].mobile_slider != None:
					dic['mobile_slider'] = domain_name + str(record[0].mobile_slider)
				else:
					dic['mobile_slider'] = ''


				if record[0].carousel_image != None:
					dic['carousel_image'] = domain_name + str(record[0].carousel_image)
				else:
					dic['carousel_image'] = ''

				if record[0].carousel_image1 != None:
					dic['carousel_image1'] = domain_name + str(record[0].carousel_image1)
				else:
					dic['carousel_image1'] = ''
				dic['carousel_text'] = record[0].carousel_text
				dic['carousel_text1'] = record[0].carousel_text1
				dic['health_text'] = record[0].health_text
				dic['promotions_url'] = record[0].promotions_url
				dic['is_promotions'] = record[0].is_promotions
				if record[0].health_image != None:
					dic['health_image'] = domain_name + str(record[0].health_image)
				else:
					dic['health_image'] = ''
				dic["promotions_image"] = []
				pimg = HomepagePromotion.objects.filter(homepage_id=record[0].id)
				if pimg.count() > 0:
					for index in pimg:
						full_path = addr_set()
						fimgs = full_path+str(index.promotions_image)
						dic["promotions_image"].append(fimgs)
				else:
					pass
				final_result.append(dic)
			return Response({
						"success": True, 
						"data": final_result,
						})
		except Exception as e:
			print("Page action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class DashboardData(APIView):
	"""
	Brand Dashboard retrieval GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Brand Dashboard data within brand.

		params: {

			"start_date" : "2021-05-17 0:00:00"
			"end_date"   : "2021-05-17 16:15:33"
		}

		Response: {

			"success": True, 
			"message": "Brand Dashboard analysis api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['company'] = cid
			s_date = dateutil.parser.parse(data['start_date'])
			e_date = dateutil.parser.parse(data['end_date'])
			cdata = Order.objects.filter(Q(order_time__lte=e_date),Q(order_time__gte=s_date)
					,Q(Company_id=cid),Q(order_status_id=6))
			final_result = {}
			if cdata.count() > 0:
				total_sale = cdata.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
				final_result['order_count'] = total_sale[0]['order_count']
				final_result['total_sale']  = round(total_sale[0]['total_revenue'],2)
			else:
				final_result['order_count'] = 0
				final_result['total_sale']  = 0
			ws = WebsiteStatistic.objects.filter(Q(created_at__lte=e_date),Q(created_at__gte=s_date)
					,Q(company_id=cid),Q(visitors=1))
			if ws.count() > 0:
				final_result['no_of_visitiors'] = ws.count() // 3 
			else:
				final_result['no_of_visitiors'] = 0
			return Response({
						"success": True, 
						"message": "Brand Dashboard analysis api worked well!!",
						"data" : final_result
						})

		except Exception as e:
			print("Dashboard Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class OutOfRangeData(CreateAPIView):
	"""
	Company(key/Door) Retrieve API View

		Service usage and description : This API is used to retrieve company info.
		Authentication Required : YES
	"""

	serializer_class = OutOfRangeSerializer
	queryset = OutOfRange.objects.all()




class SourceReportData(APIView):
	"""
	Order Source Report POST API

		Authentication Required		: Yes
		Service Usage & Description	: Order Source Report POST

		Data Post: {
			"start_date" :""
			"end_date" : ""
		}
		Response: {
			"success": True, 
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					raise Exception("Validity dates are not valid!!")
			user = request.user.id
			cid = get_user(user)
			orderdata = []
			que = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date),\
									Q(Company=cid),Q(order_status_id=6))
			tevenue = que.values('order_source').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
			if tevenue.count() > 0:
				for index in tevenue:
					temp = {}
					temp['order_source'] = OrderSource.objects.filter(id=index['order_source'])[0].source_name
					temp['total_sale'] = round(index['total_revenue'],2)
					temp['order_count'] = index['order_count']
					orderdata.append(temp)
			return Response({
						"success": True,
						"data" : orderdata
						})

		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
			

class DateWiseReport(APIView):
	"""
	Order Source Report POST API

		Authentication Required		: Yes
		Service Usage & Description	: Order Source Report POST

		Data Post: {
			"start_date" :""
			"end_date" : ""
		}
		Response: {
			"success": True, 
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					raise Exception("Validity dates are not valid!!")
			user = request.user.id
			cid = get_user(user)
			orderdata = []
			que = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date),\
								Q(Company=cid),Q(order_status_id=6))
			li = []
			for index in que:
				order_time = index.order_time
				li.append(order_time.date())
			finaldate = set(li)
			for index in sorted(finaldate):
				odata = que.filter(order_time__date=index)
				tevenue = odata.values('outlet').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
				if len(tevenue) > 0:
					for i in tevenue:
						temp = {}
						temp['date'] = odata[0].order_time.isoformat()
						outlet = i['outlet']
						temp['outlet'] = OutletProfile.objects.filter(id=outlet)[0].Outletname
						temp['total_sale'] = i['total_revenue']
						temp['order_count'] = i['order_count']
						orderdata.append(temp)
			return Response({
						"success": True,
						"data" : orderdata
						})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
			

class PaymentReportData(APIView):
	"""
	Order Source Report POST API

		Authentication Required		: Yes
		Service Usage & Description	: Order Source Report POST

		Data Post: {
			"start_date" :""
			"end_date" : ""
		}
		Response: {
			"success": True, 
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					raise Exception("Validity dates are not valid!!")
			user = request.user.id
			cid = get_user(user)
			orderdata = []
			que = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date),\
									Q(Company=cid),Q(order_status_id=6))
			# que = Order.objects.filter(Q(Company=cid),Q(order_status_id=6))
			cod = 0 
			cod_count = 0
			google_pay = 0
			google_pay_count = 0
			online_paid = 0
			online_paid_count = 0
			paytm = 0
			paytm_count = 0
			razorpay = 0
			razorpay_count = 0
			payu = 0
			payu_count = 0
			upi = 0
			upi_count = 0
			edc_machine = 0
			edc_machine_count = 0
			zonline = 0
			zonline_count = 0
			sonline = 0
			sonline_count = 0
			total_amount =0
			order_count =0
			for i in que:
				if i.settlement_details !=None and len(i.settlement_details) > 0:
					k = 1
					for k in i.settlement_details:
						pdata = PaymentMethod.objects.filter(id=k['mode'])
						if pdata.count() > 0:
							pmode = pdata[0].payment_method
							if pmode == 'Swiggy Online':
								c = k['amount']
								sonline = round(sonline + float(c),2)
								sonline_count = sonline_count + 1
							else:
								pass
							if pmode == 'Zomato Online':
								c = k['amount']
								zonline = round(zonline + float(c),2)
								zonline_count = zonline_count + 1
							else:
								pass
							if pmode == 'EDC Machine':
								c = k['amount']
								edc_machine = round(edc_machine + float(c),2)
								edc_machine_count = edc_machine_count + 1
							else:
								pass
							if pmode == 'UPI':
								c = k['amount']
								upi = round(upi + float(c),2)
								upi_count = upi_count + 1
							else:
								pass
							if pmode == 'Razorpay':
								c = k['amount']
								razorpay = round(razorpay + float(c),2)
								razorpay_count = razorpay_count + 1
							else:
								pass
							if pmode == 'Cash':
								c = k['amount']
								cod = round(cod + float(c),2)
								cod_count = cod_count + 1
							else:
								pass
							if pmode == 'Online Paid':
								c = k['amount']
								online_paid = round(online_paid + float(c),2)
								online_paid_count = online_paid_count + 1
							else:
								pass
			p_list ={}
			p_list['payment_mode'] = 'Cash'
			p_list['total_sale'] = cod
			p_list['total_order'] = cod_count
			orderdata.append(p_list)

			p_list1 = {}
			p_list1['payment_mode'] = 'Online Paid'
			p_list1['total_sale'] = online_paid
			p_list1['total_order'] = online_paid_count
			orderdata.append(p_list1)


			p_list2 = {}
			p_list2['payment_mode'] = 'PayTm'
			p_list2['total_sale'] = paytm
			p_list2['total_order'] = paytm_count
			orderdata.append(p_list2)


			p_list3 = {}
			p_list3['payment_mode'] = 'Google Pay'
			p_list3['total_sale'] = google_pay
			p_list3['total_order'] = google_pay_count
			orderdata.append(p_list3)

			p_list4 = {}
			p_list4['payment_mode'] = 'PayU'
			p_list4['total_sale'] = payu
			p_list4['total_order'] = payu_count
			orderdata.append(p_list4)


			p_list5 = {}
			p_list5['payment_mode'] = 'Razorpay'
			p_list5['total_sale'] = razorpay
			p_list5['total_order'] = razorpay_count
			orderdata.append(p_list5)


			p_list6 = {}
			p_list6['payment_mode'] = 'UPI'
			p_list6['total_sale'] = upi
			p_list6['total_order'] = upi_count
			orderdata.append(p_list6)


			p_list7 = {}
			p_list7['payment_mode'] = 'EDC Machine'
			p_list7['total_sale'] = edc_machine
			p_list7['total_order'] = edc_machine_count
			orderdata.append(p_list7)

			p_list8 = {}
			p_list8['payment_mode'] = 'Zomato Online'
			p_list8['total_sale'] = zonline
			p_list8['total_order'] = zonline_count
			orderdata.append(p_list8)


			p_list9 = {}
			p_list9['payment_mode'] = 'Swiggy Online'
			p_list9['total_sale'] = sonline
			p_list9['total_order'] = sonline_count
			orderdata.append(p_list9)

			return Response({
						"success": True,
						"data" : orderdata
						})

		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
			



# class EventData(APIView):
	"""
	Event Report POST API

		Authentication Required		: Yes
		Service Usage & Description	: Event Data

		Data Post: {
			"start_date" :""
			"end_date" : ""
		}
		Response: {
			"success": True, 
			"data": final_result
		}

	"""
	# permission_classes = (IsAuthenticated,)
	# def post(self, request, format=None):
	# 	try:
	# 		mutable = request.POST._mutable
	# 		request.POST._mutable = True
	# 		data = request.data
	# 		if data["start_date"] != '' and data["end_date"] != '':
	# 			start_date = dateutil.parser.parse(data["start_date"])
	# 			end_date = dateutil.parser.parse(data["end_date"])
	# 			if start_date > end_date:
	# 				raise Exception("Validity dates are not valid!!")
	# 		user = request.user.id
	# 		cid = get_user(user)
	# 		orderdata = []
	# 		event_data = PrimaryEventType.objects.filter(active_status=1)
	# 		for index in event_data:
	# 			temp = {}
	# 			log_data = Logs.objects.filter(Q(event_time__lte=end_date),\
	# 				Q(event_time__gte=start_date),Q(Company_id=cid),Q(trigger_id=index.id))
	# 			if log_data.count() > 0:
	# 				temp[index.event_type] = []
	# 				for i in log_data:
	# 					dic = {}
	# 					dic['event_name'] = i.event_name
	# 					dic['event_by']  = i.event_by
	# 					e_time = i.event_time+timedelta(hours=5,minutes=30)
	# 					dic['event_time'] = e_time.isoformat()
	# 					dic['outlet'] = i.outlet.Outletname if i.outlet_id else print('')
	# 					dic['order_status'] = i.order_status.Order_staus_name if i.order_status else print('')
	# 					dic['order_id'] = i.order_id
	# 					temp[index.event_type].append(dic)
	# 			orderdata.append(temp)
	# 		return Response({
	# 					"success": True,
	# 					"data" : orderdata
	# 					})

	# 	except Exception as e:
	# 		print(e)
	# 		return Response(
	# 					{"error":str(e)}
	# 					)
			


class EventData(APIView):
	"""
	Event Report POST API

		Authentication Required		: Yes
		Service Usage & Description	: Event Data

		Data Post: {
			"page_no": 1,
			"page_size": 10,
			"start_date" :""
			"end_date" : ""
		}
		Response: {
			"success": True, 
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			p_no   = data["page_no"]
			p_size = data["page_size"]
			page_no = 1
			page_size = 10
			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					raise Exception("Validity dates are not valid!!")
			user = request.user.id
			cid = get_user(user)
			orderdata = []

			query = Logs.objects.filter(Q(event_time__lte=end_date),\
				Q(event_time__gte=start_date),Q(Company_id=cid)).order_by('-id')
			
			if p_no != None:
				page_no = int(data["page_no"])
			if p_size != None:
				page_size = int(data["page_size"])
			try:
				if page_size > 200:
					page_size = 200
				pages = Paginator(query, page_size)
				query_data = pages.page(page_no)
			except PageNotAnInteger:
				page_no = 1
				query_data = pages.page(page_no)
			except EmptyPage:
				page_no = pages.num_pages
				query_data = pages.page(page_no)
			page_count = pages.count
			page_info = {
				"page_no": page_no,
				"page_size": page_size,
				"total_pages" : pages.num_pages
			}
			final_data = []
			if len(query_data.object_list) > 0:
				for i in range(len(query_data.object_list)):
					dic = {}
					dic['id'] = query_data[i].id
					dic['event_name'] = query_data[i].event_name
					dic['event_by']  = query_data[i].event_by
					e_time = query_data[i].event_time+timedelta(hours=5,minutes=30)
					dic['event_time'] = e_time.isoformat()
					dic['outlet'] = query_data[i].outlet.Outletname if query_data[i].outlet_id else print('')
					dic['order_status'] = query_data[i].order_status.Order_staus_name if query_data[i].order_status else print('')
					dic['order_id'] = query_data[i].order_id
					orderdata.append(dic)
			return Response({
						"success": True,
						"data" : orderdata,
						"page": page_info,
						})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
			


class ReviewData(CreateAPIView):
	"""
	Review Creation POST API View

		Service usage and description : This API is used to create a review.
		Authentication Required : YES

		Request Body Data :
		{
			"company" 			: "1",                                     
			"outlet"            : "1"                                        
			"customer"          : "1"	
			"rating"            :
			"review"	
			"product"	        : 1	
			}					  
	"""
	serializer_class = ReviewMasterSerializer

	


class LinkedAccsPaymentsPaid(APIView):
    """
        GET API to fetch list of all payments received by a Linked Account

        Authentication Required : NO

        Request Params (GET)
        {
            "brand" : 110,
        }   
    """

    def get(self,request): 
        brand_id = self.request.GET.get('brand')
        brand = Company.objects.filter(id=brand_id)
        if brand.count()!=0:
            acc = LinkedAccount.objects.filter(brand=brand[0])
            if acc.count():
                acc = acc[0]
                key = settings.RAZORPAY_KEY
                secret = settings.RAZORPAY_SECRET
                header = {"X-Razorpay-Account":acc.acc_id,"Accept": "application/json","User-agent": "curl/7.43.0"}
                response = requests.get("https://api.razorpay.com/v1/payments",headers=header,auth=(key, secret))
                data = response.json()
                print(data)
                return Response(data, status=HTTP_200_OK)
            else:
                return Response({"message":"No linked acc found with brandId {}".format(brand_id)},status=HTTP_404_NOT_FOUND)
        return Response({"message":"No brand found with Id {}".format(brand_id)},status=HTTP_404_NOT_FOUND)     


class LinkedAccsPayments(APIView):
    """
        GET API to fetch list of all payments received by a Linked Account

        Authentication Required : NO

        Request Params (GET)
        {
            "brand" : 110,
        }   
    """

    def get(self,request): 
        brand_id = self.request.GET.get('brand')
        brand = Company.objects.filter(id=brand_id)
        if brand.count()!=0:
            routetrack = RouteTrack.objects.filter(brand=brand[0])
            if routetrack.count():
                serializer = RouteTrackSerializer(routetrack,many=True)
                return Response(data=serializer.data, status=HTTP_200_OK)
            else:
                return Response({"message":"No linked acc found with brandId {}".format(brand_id)},status=HTTP_404_NOT_FOUND)
        return Response({"message":"No brand found with Id {}".format(brand_id)},status=HTTP_404_NOT_FOUND)     



def send_payment_link(cost, plan_name, customer, key, secret,customer_eionpay=None):
    try:
        url = "https://api.razorpay.com/v1/invoices"
        data = {}
        data["type"] = "link"
        data["amount"] = int(cost) * 100
        data["view_less"] = 1
        data["currency"] = "INR"
        if customer_eionpay is None:
            data["description"] = "You have requested a subscription for the Aizo Contactless menu's {} plan".format(
                plan_name
            )
        else:
            if plan_name is not None:
                data["description"] = "You have been imposed with a bill for your order : {}".format(
                    plan_name
                )   
            else:
                data["description"] = "You have been imposed with a bill from Eoraa Consulting."
        data["customer"] = {}
        data["customer"]["name"] = customer["name"]
        data["reminder_enable"] = True
        if customer["email"]:
            data["customer"]["email"] = customer["email"]
            data["email_notify"] = 1
        if customer["contact"]:
            data["customer"]["contact"] = customer["contact"]
            data["sms_notify"] = 1
        

        data = json.dumps(data)
        headers = {"Content-type": "application/json"}
        response = requests.post(
            url,
            data=data,
            headers=headers,
            auth=(key, secret),
        )


        data = json.loads(response.content.decode(encoding="utf-8"))
        print("done", type(data), data["id"])
        return data["id"]
    except Exception as e:
        print(e)
        return 0

class EionPayAPI(APIView):
    """
    {
        "brand" : 1,
        "upi_link": "true", // if upi payments are required. if False can accept all modes.
        "amount": 100,
        "currency": "INR",
        "description": "Payment for 1 burger and 2 frenchfries",
        "customer": {
            "name": "Karre Kamal",
            "contact": "+918247707332",
            "email": "karrekamal10@gmail.com"
        }
    }
    """

    @transaction.atomic()
    def post(self, request):
        req_data = request.data
        try:
            key = settings.RAZORPAY_KEY
            secret = settings.RAZORPAY_SECRET
            if "description" not in req_data:
                req_data["description"] = None
            send_link = send_payment_link(
                req_data["amount"],
                req_data["description"],
                req_data["customer"],
                key,
                secret,
                customer_eionpay = 1
            )
            if send_link:
                brand = Company.objects.get(id=req_data["brand"])
                cust_dic = {}
                cust_dic["Name"] = req_data["customer"]["name"]
                if "contact" in req_data["customer"]:
                    cust_dic["contact"] = req_data["customer"]["contact"]
                if "email" in req_data["customer"]:
                    cust_dic["email"] = req_data["customer"]["email"]
                route_track = RouteTrack.objects.create(
                    brand=brand, 
                    Payment_link_id=send_link,
                    customer_details=cust_dic,
                    amount=req_data["amount"],
                    reference_id="Ref_"+str(uuid.uuid4())[:10],
                    currency=CurrencyMaster.objects.get(currency="INR"),
                    Order_description=req_data["description"]
                )
                return Response(
                    data={"id": send_link},
                    status=HTTP_200_OK,
                )
            else:
                return Response(status=HTTP_417_EXPECTATION_FAILED)
        except Exception as e:
            return Response({"message":str(e)},status=HTTP_500_INTERNAL_SERVER_ERROR)


