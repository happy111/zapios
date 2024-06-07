from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
import json
from rest_framework import serializers
from ZapioApi.api_packages import *
from Orders.models import Order, OrderStatusType,OrderTracking
from rest_framework.authtoken.models import Token
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from datetime import datetime
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
from rest_framework_tracking.mixins import LoggingMixin
from Outlet.models import OutletProfile,DeliveryBoy
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from History.models import Logs
from Event.models import PrimaryEventType


class LogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Logs
		fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class orderNotificationCount(APIView):
	"""
	New Order Notification Count and list order Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for count for Order and list new order  within POS

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			is_outlet = OutletProfile.objects.filter(auth_user_id=user)
			is_brand = Company.objects.filter(auth_user_id=user)
			is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			alloutlet = []
			if is_cashier.count() > 0:
				m =  ManagerProfile.objects.filter(auth_user_id=user)
				cid =m[0].Company_id
				outlet = m[0].outlet
				for i in outlet:
					alloutlet.append(i)
			else:
				pass
			if is_outlet.count() > 0:
				o = OutletProfile.objects.filter(auth_user_id=user)
				cid = o[0].Company_id
				p = OutletProfile.objects.filter(id=o[0].id)
				for i in p:
					alloutlet.append(i.id)
			else:
				pass
			if is_brand.count() > 0:
				outlet = Company.objects.filter(auth_user_id=user)
				cid = outlet[0].id
				p = OutletProfile.objects.filter(Company_id=cid)
				for i in p:
					alloutlet.append(i.id)
			else:
				pass
			now = datetime.now()
			todate = now.date()
			ord_data =[]
			for i in alloutlet:
				order_record = Order.objects.filter(Q(order_time__date=todate),\
					Q(Company_id=cid),Q(is_accepted=0),Q(outlet_id=i)).order_by('-order_time')
				if order_record.count() > 0:
					for i in order_record:
						p_list ={}
						add = i.address
						p_list['id'] = i.id
						p_list['customer'] = i.customer
						p_list['delivery_address'] = i.address
						p_list['special_instructions'] = i.special_instructions
						p_list['order_id'] = i.outlet_order_id
						p_list['order_status'] = i.order_status_id
						p_list['discount_value'] = i.discount_value
						p_list['sub_total'] = i.sub_total
						p_list['total_bill_value'] = i.total_bill_value
						o_time = i.order_time+timedelta(hours=5,minutes=30)
						p_list['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
						p_list['delivery_time'] = i.delivery_time
						if p_list['delivery_time'] != None:
							d_time = i.delivery_time+timedelta(hours=5,minutes=30)
							p_list['delivery_time'] = d_time.strftime("%d/%b/%y %I:%M %p")
						else:
							p_list['delivery_time'] = None
						if  i.payment_mode == '0':
							p_list['payment_mode'] = "Cash on Delivery"
						else:
							p_list['payment_mode'] = "Online"
						order_status_rec = OrderStatusType.objects.filter(id=i.order_status_id)
						if order_status_rec.count() != 0:
							p_list['order_status_name'] =\
							order_status_rec.first().Order_staus_name
							p_list['color_code'] = order_status_rec.first().color_code
						else:
							return Response(
								{"message":"Order Status Configuration data is not set in backend!!"})
						p_list["can_process"] = True
						if i.order_status.can_process == 1:
							pass
						else:
							p_list["can_process"] = False
						if i.outlet !=None:
							p_list["outlet_name"] = i.outlet.Outletname
						else:
							pass
						if i.order_source == None:
							p_list['source'] = "Website"
						else:
							p_list['source'] = i.order_source
						p_list['is_accepted'] = i.is_accepted
						ord_data.append(p_list)
					countorders = order_record.count()
				else:
					countorders = 0
				order_record.update(is_accepted=1)
			return Response({"status":True,
							"orderdetails" : ord_data,
							"ordercount": countorders })

		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)

class orderAccepted(LoggingMixin,APIView):
	"""
	Accepted / Cancel Order All POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to accepted / cancel order.

		Data Post: {
			"id"                   : "95",
			"is_accepted"		   : "false",
			"order_cancel_reason"  : "dddddddddd"
		}

		Response: {

			"success": True, 
			"message": "Accepted Updated Successfully",

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			order_record = Order.objects.filter(id=data['id'])
			user = request.user.id
			cid = get_user(user)
			err_message = {}
			postdata = {}
			if data["is_accepted"] == "true":
				pass
			elif data["is_accepted"] == "false":
				pass
			else:
				err_message["is_accepted"] = "Active status data is not valid!!"
			if order_record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Order data is not valid to Accepted!!"
				}
				)
			else:
				data["updated_at"] = datetime.now()
				if data["is_accepted"] == "true":
					data['order_status'] = 2
					info_msg = "Order is accepted successfully!!"
				else:
					err_message["order_cancel_reason"] = \
								validation_master_anything(data["order_cancel_reason"],"Cancel reason",
								alpha_re,3)
					if any(err_message.values())==True:
						return Response({
							"success": False,
							"error" : err_message,
							"message" : "Please correct listed errors!!"
							})
					data['order_status'] = 7
					data['order_cancel_reason'] = data['order_cancel_reason']
					info_msg = "Order is cancelled successfully!!"
		
				serializer = \
				OrderSerializer(order_record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
					order_tracking = OrderTracking.objects.create(order_id=data['id'], 
						Order_staus_name_id=data['order_status'], created_at=datetime.now())
					postdata['order_id'] = order_record[0].order_id
					postdata['auth_user']  = user
					postdata['Company']  = cid
					postdata['event_by'] = ManagerProfile.objects.filter(auth_user_id=user)[0].username
					postdata['count']  = 1
					postdata['relevance']  = '50'
					postdata['order_status']  = 7
					postdata['event_name']  = OrderStatusType.objects.filter(id=7)[0].Order_staus_name
					postdata['trigger']  = PrimaryEventType.objects.filter(event_type=postdata['event_name'])[0].id

					postdata['reason'] = 	data['order_cancel_reason']
					log_serializer = LogSerializer(data=postdata)
					if log_serializer.is_valid():
						data_info = log_serializer.save()
					else:
						priint("something went wrong",log_serializer.errors)
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
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print(e)





class orderNotificationSeen(APIView):
	"""
	All Order Notification  Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for not seen order.

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			now = datetime.now()
			todate = now.date()
			data = request.data
			orderdata = Order.objects.filter(Q(order_time__date=todate))
			if orderdata.count() > 0:
				is_outlet = OutletProfile.objects.filter(auth_user_id=user)
				is_brand = Company.objects.filter(auth_user_id=user)
				is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
				alloutlet = []
				if is_cashier.count() > 0:
					if len(data['brand']) > 0:
						for index in data['brand']:
							co_id = ManagerProfile.objects.filter(mobile=is_cashier[0].mobile,Company_id=index)
							if co_id.count() > 0:
								for temp in co_id[0].outlet:
									alloutlet.append(temp)
					else:
						m =  ManagerProfile.objects.filter(auth_user_id=user)
						cid =m[0].Company_id
						outlet = m[0].outlet
						if outlet !=None:
							for i in outlet:
								alloutlet.append(i)
						else:
							pass
				else:
					pass
				if is_outlet.count() > 0:
					o = OutletProfile.objects.filter(auth_user_id=user)
					cid = o[0].Company_id
					p = OutletProfile.objects.filter(id=o[0].id)
					for i in p:
						alloutlet.append(i.id)
				else:
					pass
				if is_brand.count() > 0:
					outlet = Company.objects.filter(auth_user_id=user)
					cid = outlet[0].id
					p = OutletProfile.objects.filter(Company_id=cid)
					for i in p:
						alloutlet.append(i.id)
				else:
					pass
				ord_data =[]
				seen_count = 0
				today_order = 0
				now = datetime.now()
				todate = now.date()
				for i in alloutlet:
					orderdata = Order.objects.filter(Q(outlet_id=i),Q(order_status_id=1),\
						Q(order_time__date=todate))
					s_c = orderdata.count()
					seen_count = int(seen_count) + int(s_c)
					order_record = Order.objects.filter(Q(order_time__date=todate),\
								   Q(outlet_id=i))
					if order_record.count() > 0:
						t_o = order_record.count()
						today_order = int(today_order) + int(t_o)
					else:
						today_order = int(today_order)
				return Response({"status":True,
								"seen_count":seen_count,
								"ordercount":today_order
								})
			else:
				return Response({"status":True,
								"seen_count":0,
								"ordercount":0
								})

		except Exception as e:
			print(e)


			
