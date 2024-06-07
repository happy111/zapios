from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import requests
from rest_framework.permissions import IsAuthenticated
import json
from datetime import datetime
from rest_framework import serializers
import razorpay
from Subscription.models import SubscriptionPlanType, SubscriptionPaymentModel
from _datetime import datetime


class SubscriptionPayment(APIView):
    """
    Subscription Payment Process POST API

        Authentication Required		: No
        Service Usage & Description	: This Api is used for subscription charge.

        Data Post: {
            "amount"        : "23",
            "description" :  "Payment for add on {addon name}                   //"rzp_test_JubCA5FmcNfzDE",
            "currency":      "INR"                                              //"8Bt4zNbCnvHB693XVUeh7WDX"
            "customer": {
							"name": "company name",
							"mobile": "company contact no",
							"email" : "company email id"
						}
        }

        Response: {

            "success": True,
            "data": order_create
        }

    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            url = " https://api.razorpay.com/v1/invoices"
            data = request.data
            print("checkdata", data["description"], type(int(float(str(data["amount"])))))
            key = "rzp_test_JubCA5FmcNfzDE1"
            secret = "8Bt4zNbCnvHB693XVUeh7WDX1"
            customer = data["customer"]
            data_dict = {}
            data_dict["type"] = "link"
            data_dict["amount"] = int(float(str(data["amount"]))) * 100
            data_dict["view_less"] = 1
            data_dict["currency"] = data["currency"]
            data_dict["description"] = data["description"]
            data_dict["customer"] = {}
            data_dict["customer"]["name"] = data["customer"]["name"]
            data_dict["reminder_enable"] = True
            if customer["email"]:
                data_dict["customer"]["email"] = data["customer"]["email"]
                data_dict["email_notify"] = 1
            if customer["mobile"]:
                data_dict["customer"]["contact"] = data["customer"]["mobile"]
                data_dict["sms_notify"] = 1
            data = json.dumps(data_dict)
            headers = {'Content-type': 'application/json'}
            # session = requests.Session()
            # session.trust_env = False
            response = requests.post(url, data=data, headers=headers, auth=(key, secret) )
            print("done", response.content)
            return Response(data=response.content)
        except Exception as e:
            print("Delivery Charge Configuration retrieval Api Stucked into exception!!")
            print(e)
            return Response({
                "success": False,
                "message": "Error happened!!",
                "errors": str(e)})
