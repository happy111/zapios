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
from Product.models import Product,Tag





class AllTag(APIView):
	"""
	AddonDetails retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Order analysis as per customer data.

		Data Post: {
			"id"                   : "33234"
		}

		Response: {

			"success": True, 
			"message": "Order analysis as per customer retrieval api worked well",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			user = self.request.user.id
			Company_id = get_user(user)
			customer = CustomerProfile.objects.filter(id=data['customer_id']).order_by('-created_at')
			if customer.count() > 0:
				mobile = customer[0].id
			record = Order.objects.filter(Company_id=Company_id,users_id=mobile)
			if record.count() > 0:
				totaltag = []
				for index in record:
					order_description = index.order_description
					for k in order_description:
						if 'product_id' in k:
							product_data = Product.objects.filter(id=k['product_id'])
							if product_data.count() > 0:
								alltag = product_data[0].tags
								for t in alltag:
									totaltag.append(t)
				tag = []
				for tags in totaltag:
					tag_dict = {}
					tag_detail = Tag.objects.filter(id=tags)
					if tag_detail.count() > 0:
						tag_dict['name'] = tag_detail[0].tag_name
						tag_dict['count'] = totaltag.count(tags)
						tag.append(tag_dict)
		
				altag = []
				for k in tag:
					if k not in altag:
						altag.append(k)
			else:
				altag = []
			return Response({"status":True,
							"data":altag,
								})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


