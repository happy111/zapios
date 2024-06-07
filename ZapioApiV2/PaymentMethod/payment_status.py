import razorpay
# key = "rzp_test_3jTkM4tBkXfW2G"
# secret = "C26NE62RPuCpRrrrzWus6TOK"

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
import razorpay
# from Customers.models import Customer
from Configuration.models import PaymentStatus
# from wallet.models import Gatewaypayments, ActualWallet, CustomerWallet, WalletType
from rest_framework import serializers
import hashlib

class PaymentStatusSerailizer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = "__all__"

class PaymentStatus(APIView):
    """
    Payment Process POST API

        Authentication Required		: No
        Service Usage & Description	: This Api is used for delivery charge Configuration.

        Data Post: {
            "keyid"        : "rzp_test_el6ponmfCSuIVF",//optional
            "keySecret"    : "h4VDBg17mBds7cKc3zAMYppH",//optional
            "payment_id"     : "1313243",
            "is_success" : True
        }

        Response: {

            "success": True,
        }

    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            user_id = request.user.id
            data = request.data
            if "payment_id" in data and "is_success" in data:
                serializer = PaymentStatusSerailizer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({
                        "success": True,
                    })
            else:
                return Response({
                    "success" :False,
                    "errors": "payment_id and is_success both are required"
                })
        except Exception as e:
            print("Payment status saver Api Stucked into exception!!")
            print(e)
            return Response({
                "success": False,
                "message": "Error happened!!",
                "errors": str(e)})
