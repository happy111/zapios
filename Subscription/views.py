import razorpay
from django.shortcuts import render
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from .serializers import (
	SubscriptionSerializer,
	SubscriptionPaymentSerializer
)
from . models import *
from rest_framework.response import Response
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework.views import APIView


class PaymentConfig(ListAPIView):
	"""
	Payment Config GET API

		Service Usage and Description : This API is used to payemnt config.
		Authentication Required : YES

		Params : {

		}
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = SubscriptionPaymentSerializer
	queryset = SubscriptionPaymentModel.objects.all()


class SubscriptionListingAPI(ListAPIView):
	"""
	Subscription Listing GET API

		Service Usage and Description : This API is used to listing of subscription.
		Authentication Required : YES

		Params : {

		}
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = SubscriptionSerializer
	queryset = SubscriptionPlanType.objects.all()

	def get_queryset(self):
		queryset = SubscriptionPlanType.objects.filter(active_status=1).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = SubscriptionSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					})



class PaymentCreateAPI(APIView):
	
	"""
	Payment Process POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for payment create.

		Data Post: {
			"subscription" : "7"
			"keyid"        : "rzp_test_el6ponmfCSuIVF",
			"keySecret"    : "h4VDBg17mBds7cKc3zAMYppH",
		}

		Response: {

			"success": True, 
			"message": "API Worked properly!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = self.request.data
			company_id = get_user(request.user.id)
			client = razorpay.Client(auth=(data['keyid'], data['keySecret']))
			payment_process_record = Gatewaypayments.objects.all()
			if payment_process_record.count() == 0:
				receipt_id = "AIZO-001"
			else:
				receipt_id = "AIZO-00"+str(payment_process_record.last().id+1)
			record_create = Gatewaypayments.objects.create(
				receipt_id=receipt_id,
				subscription_id=data['subscription'],
				company_id=company_id
				)
			payment_process_data = Gatewaypayments.objects.filter(receipt_id=receipt_id)
			pay_data = {}
			s_data = SubscriptionPlanType.objects.filter(id=data['subscription'])
			pay_data["amount"]   = s_data[0].cost
			pay_data["currency"] = 'INR'
			pay_data["receipt"] = receipt_id
			pay_data["payment_capture"] = 1
			order_create = client.order.create(data=pay_data)
			payment_update = payment_process_data.update(
				razorpay_order_id=order_create['id'],
				amount=pay_data["amount"])
			return Response({
						"success": True, 
						"data" : order_create
						})
		except Exception as e:
			print("Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})



class PaymentProcess(APIView):
	
	"""
	Payment & Wallet Process POST API

		Authentication Required		: yes
		Service Usage & Description	: This Api is used for payment verification at server.

		Data Post: {
			"order_id"       : "jsdbvfsjdvbvjbfvjsfdvsbhvsdhvsdbf",
			"payment_id"     : "sjdbcjbshcbscsbhcscsbchscschscbscshcshcs",
			"signature"      : "h4VDBg17mBds7cKc3zAMYppH"
		}

		Response: {

			"success": True, 
			"message": "API Worked properly!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			company_id = get_user(request.user.id)
			order_check = Gatewaypayments.objects.filter(razorpay_order_id=data['order_id'])
			if order_check.count()==1:
				pass
			else:
				return Response({
					"success" : False,
					"message" : "Payment order id and other credentials does'nt match!!"
					})
			config_check = SubscriptionPaymentModel.objects.filter()
			config = {}
			config['keyid'] = config_check[0].key
			config['keySecret'] = config_check[0].secret
			client = razorpay.Client(auth=(config['keyid'], config['keySecret']))
			pay_data = {}
			pay_data["razorpay_order_id"] = data['order_id']
			pay_data["razorpay_payment_id"] = data['payment_id']
			pay_data["razorpay_signature"] = data['signature']
			check_signature = client.utility.verify_payment_signature(pay_data)
			if check_signature == None:
				process_update = order_check.update(is_successful=1,razorpay_payment_id=data['payment_id'])
				brand_data = Company.objects.filter(id=company_id)
				brand_updata = brand_data.update(plan_name_id=order_check[0].subscription_id)

				return Response({
					"success" : True,
					"message" : "Payment is successfull."
					})
			else:
				return Response({
					"success" : False,
					"message" : "Payment is failed due to some reason..."\
					+" If money is deducted from your acccount..It will be refunded within 2-3 working days."
					})
		except Exception as e:
			print("Api Stucked into exception!!")
			print(e)
			return Response({
							"success" : False, 
							"message" : "Error happened!!", 
							"errors"  : str(e)
							})
















