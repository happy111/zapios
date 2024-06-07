import calendar
import time
from datetime import datetime
from django.db.models import Q
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from datetime import datetime, timedelta
from Orders.models import *
from rest_framework import serializers
from Configuration.models import UserExperience

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperience
        fields = "__all__"


class CustomeRating(APIView):
	"""
	Schedule order  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to profile details.

		Data Post: {

			"email"	    :	"umeshsamal3@gmail.com",


		}

		Response: {

			"status"				: True,

		}

	"""
	def post(self,request):
		try:
			data = request.data
			order_data = Order.objects.filter(outlet_order_id=data['order_id'])
			if order_data.count() > 0:
				post_data = {}
				customer = order_data[0].customer
				if 'email' in customer:
					post_data['email'] = customer['email']
				else:
					post_data['email'] = ''
				if 'mobile_number' in customer:
					post_data['mobile'] = customer['mobile_number']
				else:
					post_data['mobile'] = ''
				post_data['rating'] = data['rating']
				post_data['company'] = order_data[0].Company_id
				ratingSerializer = RatingSerializer(data=post_data)
				if ratingSerializer.is_valid():
					ratingSerializer.save()
				else:
					print(ratingSerializer.errors)
				return Response({
					"success": True,
				   })
		except Exception as e:
			print(e)