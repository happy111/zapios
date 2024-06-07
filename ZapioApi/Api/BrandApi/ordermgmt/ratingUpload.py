from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime, timedelta
from Orders.models import Order,OrderStatusType
from Product.models import Product
from rest_framework import serializers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import RetrievalData
import pandas as pd
import os


class BulkRatingUpdate(APIView):
	"""
	Order Bulk Rating Update POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to update buk rating order data through XLS.

		Data Post: {
			"rating_xls"                   : "rating.xls"
		}

		Response: {

			"success": True, 
			"message": "Order data Updated Successfully!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			ext = os.path.splitext(data["rating_xls"].name)[1]
			if ext == ".xls":
				pass
			else:
				return Response({
					"success" : False,
					"message" : "Uploaded file is not in xls format!!"
					})
			data_frame =  pd.read_excel(data["rating_xls"])
			try:
				filter_data = data_frame.filter(["Order Id", "Rating"])
			except Exception as e:
				return Response({
					"success" : False,
					"message" : "Provided Xls file is not having valid column!!"
					}) 
			for index, row in filter_data.iterrows():
				if pd.isnull(row['Rating'])==True:
					pass
				else:
					try:
						row["Rating"] = float(row["Rating"])
					except Exception as e:
						return Response({
							"success" : False,
							"message" : "Rating value in uploaded xls is not valid!!"
							})
					data_update = \
					Order.objects.filter(order_id=row["Order Id"]).update(rating=row["Rating"])
			return Response({
						"success" : True,
						"message" : "Rating is updated Successfully!!"
						})	
		except Exception as e:
			print("Order data retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success" : False,
							"message" : "API Stucked in exception!!"
							})