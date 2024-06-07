from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
import json
#Serializer for api
from rest_framework import serializers
from Orders.models import Order,OrderStatusType, OrderTracking,QuantityWiseOrderProcess
from rest_framework.authtoken.models import Token
from Outlet.models import DeliveryBoy,OutletProfile
from Outlet.Api.serializers.order_serializers import OrderSerializer
from django.db.models import Q
from datetime import datetime, timedelta
from zapio.settings import Media_Path
from _thread import start_new_thread
from kitchen.models import ProcessTrack,StepToprocess
from Product.models import Product,Variant

def TrackEntry_Sync(o_id):
	order_q = Order.objects.filter(id=o_id)
	order_description = order_q[0].order_description
	company_id = order_q[0].Company_id
	outlet_id = order_q[0].outlet_id
	for i in order_description:
		p_id = i["id"]
		if i["size"] != "N/A":
			v_id = Variant.objects.filter(variant__exact=i['size'],Company=company_id)[0].id
		else:
			v_id = None
		steps_q = StepToprocess.objects.filter(company=company_id,product=p_id)
		if v_id != None:
			steps_q = steps_q.filter(varient=v_id)
		else:
			pass
		if steps_q.count()!=0:
			for q in steps_q:
				track_q = ProcessTrack.objects.filter(Step=q.id,Order=o_id)
				if track_q.count()==0:
					track_create = \
					ProcessTrack.objects.create(company_id=company_id,Step_id=q.id,Order_id=o_id,\
										product_id=p_id,process_status="2",Variant_id=v_id)
				else:
					track_updated = \
					track_q.update(Variant=v_id)
		else:
			pass
	return "Order Track Entry synchronized successfully!!"



class ProductWiseOrderListing(APIView):
	"""
	Order listing Product wise GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the details of pending orders product wise for particular outlet.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			user = request.user.id
			data = \
			Order.objects.filter(outlet__auth_user=user,
				order_status__Order_staus_name__iexact="Received").order_by('order_time')
			if data.count() > 0:
				for i in data:
					p_list ={}
					p_list["order_id"] = i.id
					p_list["order_description"] = i.order_description
					for t in p_list["order_description"]:
						pro_id = t['id']
						if "size" not in t:
							t["size"] = "N/A"
						if t["size"] != "N/A":
							v_id = Variant.objects.filter(variant=t['size'])[0].id
						else:
							v_id = None
						if "quantity" not in t:
							qty = 1
						else:
							qty = t['quantity']
						for k in range(1,qty+1):
							ch_u = QuantityWiseOrderProcess.objects.filter(order_id=i.id,\
									product_id=pro_id,variant_id=v_id,
									quantity=k)
							if ch_u.count() ==  0:
								p_query = QuantityWiseOrderProcess.objects.create(order_id=i.id,\
									product_id=pro_id,variant_id=v_id,
									quantity=k,created_at=datetime.now())
							else:
								pass
			else:
				return Response({"status":True,
							    "data":"No new order right now!!"})
			final_result =[]
			company_id = data[0].Company_id
			for i in data:
				p_list ={}
				p_list["order_id"] = i.id
				a = i.order_description
				p_list['details'] = []
				for t in a:
					if "quantity" not in t:
						qty = 1
					else:
						qty = t['quantity']
					for k in range(1,qty+1):
						s = {}
						s["id"]		= t['id']
						s["name"]		= t['name']
						s["price"]		= t['price']
						s["size"]		= t['size']
						quan_q = \
						QuantityWiseOrderProcess.objects.filter(order_id=i.id,product_id=s["id"],quantity=k)
						s["quan_id"]		= quan_q[0].id
						s["quantity"]		= quan_q[0].quantity
						s["customization_details"] = t['customization_details']
						q = Product.objects.filter(id=t["id"])[0]
						if q.product_image != None and q.product_image != "":
							s["product_image"] = Media_Path+str(q.product_image)
						else:
							s["product_image"] = None
						if "size" not in t:
							s["size"] = "N/A"
						else:
							pass
						if t["size"] != "N/A":
							s["v_id"] = \
							Variant.objects.filter(variant__exact=t['size'],Company=company_id)[0].id
						else:
							s["v_id"] = None
						if s["v_id"] == None:
							process_rec  = \
							ProcessTrack.objects.filter(Order=p_list["order_id"],product=t["id"])
						else:
							process_rec  = \
							ProcessTrack.objects.filter(Order=p_list["order_id"],product=t["id"],\
										Variant=s["v_id"])
						if process_rec.count()==0:
							s["product_status"] = 2
						else:
							s["product_status"] = process_rec[0].process_status
						if quan_q[0].active_status == False:
							p_list['details'].append(s)
						else:
							pass
				final_result.append(p_list)
			start_new_thread(TrackEntry_Sync, (p_list["order_id"],))
			return Response({"status":True,
							"data":final_result})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)