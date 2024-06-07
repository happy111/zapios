from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, ActionSync, ProductSync, CatSync


class OutletItems(APIView):
	"""
	Synced Products listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing synced products with urbanpiper within brand.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"data" : result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			data = request.data
			record = OutletSync.objects.filter(outlet_id=data["outlet_id"],sync_status="synced")
			if record.count() == 0:
				return ({
					"status" : False,
					"message" : "This outlet is not valid to proceed!!"
					})
			else:
				result =[]
				product_q = ProductSync.objects.filter(Q(sync_outlet=record[0].id),\
														~Q(sync_status='not_intiated'))
				if product_q.count() != 0:
					for i in product_q:
						record_dict ={}
						record_dict['id'] = i.id
						record_dict['p_id'] = i.product_id
						variant = i.variant
						if variant != None:
							record_dict['product'] = i.product.product_name+" | "+i.variant.variant
						else:
							record_dict['product'] = i.product.product_name
						result.append(record_dict)
				else:
					pass
				return Response({"status":True,
								"data":result})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)