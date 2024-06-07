from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from Product.models import Tag,Product,ProductCategory,Variant,FoodType
from ZapioApi.Api.BrandApi.tag.serializer import TagSerializer
from Brands.models import Company
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user



def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name


class TagList(APIView):

	"""
	Tag listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Tag data.
	"""


	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			user = request.user.id
			cid = get_user(user)
			alltag = Tag.objects.filter()
			final_result = []
			if alltag.count() > 0:
				for i in alltag:
					alltag = {}
					alltag['tag_name'] = i.tag_name
					alltag['id'] = i.id
					alltag['active_status'] = i.active_status
					img = i.tag_image
					domain_name = addr_set()
					if img != "" and img != None and img != "null":
						full_path = domain_name + str(img)
						alltag['tag_image'] = full_path
					else:
						alltag['tag_image'] = ''
					final_result.append(alltag)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Tag listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})