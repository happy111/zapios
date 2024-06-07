from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Outlet.models import DeliveryBoy,OutletProfile
from ZapioApi.api_packages import *
from rest_framework import serializers
from Orders.models import Order
from UserRole.models import ManagerProfile
from History.models import RiderHistory

class RiderSerializer(serializers.ModelSerializer):
	class Meta:
		model = ManagerProfile
		fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
	class Meta:
		model = RiderHistory
		fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class AsignRider(APIView):
	"""
	Assign rider POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to assign rider for order id.

		Data Post: {
			
			"order_id"     : "1",
			"rider_id"   : "1"
		}

		Response: {

			"success" : True,
			"message" : "Rider listing worked well!!",
			"data"    : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			data["order"] = str(data["order_id"])
			data["rider"] = str(data["rider_id"])
			user = request.user.id
			rider = {}
			riderlog = {}
			orderlog = {}
			err_message = {}
			fd = ManagerProfile.objects.filter(auth_user_id=user)
			cid = fd[0].Company_id
			err_message["order"] = \
					validation_master_anything(data["order"],
					"Order Id",contact_re, 1)
			err_message["rider"] = \
					validation_master_anything(data["rider"],
					"Rider Id",contact_re, 1)
			order_record = Order.objects.filter(id=data['order'])
			if order_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required order data is not valid!!"
				}
				)
			else:
				if order_record[0].is_rider_assign == 1:
					logdata = RiderHistory.objects.filter(order_id_id=data['order_id'])
					alld = ManagerProfile.objects.filter(id=data['rider'])
					rider['is_assign'] = 1
					rider["updated_at"] = datetime.now()
					rider_serializer = RiderSerializer(alld[0],data=rider,partial=True)
					if rider_serializer.is_valid():
						data_info = rider_serializer.save()
						riderlog['Rider'] = int(data['rider'])
						riderlog['order_id'] = int(data['order'])
						riderlog['Company'] = cid
						riderlog['outlet'] = order_record[0].outlet_id
						log_serializer = LogSerializer(logdata[0],data=riderlog,partial=True)
						if log_serializer.is_valid():
							data = log_serializer.save()
							orderlog['delivery_boy'] = alld[0].id
							orderlog['is_rider_assign'] = 1
							order_serializer = OrderSerializer(order_record[0],data=orderlog,partial=True)
							if order_serializer.is_valid():
								data_info = order_serializer.save()
								return Response({
	           					 "success":True,
								 "message":"Rider is Reassign this order!!",
								})
							else:
								print("Error",order_serializer.errors)
				else:
					pass
				alld = ManagerProfile.objects.filter(id=data['rider'])
				rider['is_assign'] = 1
				rider["updated_at"] = datetime.now()
				rider_serializer = RiderSerializer(alld[0],data=rider,partial=True)
				if rider_serializer.is_valid():
					data_info = rider_serializer.save()
					riderlog['Rider'] = int(data['rider'])
					riderlog['order_id'] = int(data['order'])
					riderlog['Company'] = cid
					riderlog['outlet'] = order_record[0].outlet_id
					log_serializer = LogSerializer(data=riderlog)
					if log_serializer.is_valid():
						data = log_serializer.save()
						orderlog['delivery_boy'] = alld[0].id
						orderlog['is_rider_assign'] = 1
						order_serializer = OrderSerializer(order_record[0],data=orderlog,partial=True)
						if order_serializer.is_valid():
							data_info = order_serializer.save()
							return Response({
           					 "success":True,
							 "message":"Rider is assign this order!!",
							})
						else:
							print("Error",order_serializer.errors)
					else:
						print("Error",log_serializer.errors)
				else:
					print("Error",rider_serializer.errors)
					return Response({
           					 "success":True,
							 "message":"No Rider Allow!!",
							 "data" : []
						})
		except Exception as e:
			print("Outletwise category listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})