from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import uuid
import json
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class APIGenerationView(APIView):
    """
        POST API for API Key generation for Aizotec User

    """
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            Company_id = get_user(request.user.id)
            brand = Company.objects.filter(id=Company_id)
            if brand.count():
                brand = brand[0]
                apikey = "api_"+str(uuid.uuid4())
                brand.api_key = apikey
                brand.save()
                return Response({"Api_Key":apikey},status=status.HTTP_200_OK)
            else:
                return Response({"msg":"Please enter valid token"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
