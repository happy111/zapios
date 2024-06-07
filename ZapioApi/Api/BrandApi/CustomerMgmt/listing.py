from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *

#Serializer for api
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from Customers.models import CustomerProfile



class UserlistingSerializer(serializers.ModelSerializer):

	def to_representation(self, instance):
		representation = super(UserlistingSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		return representation

	class Meta:
		model = CustomerProfile
		fields = '__all__'

class Userlisting(ListAPIView):
	"""
	User listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of User data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = UserlistingSerializer
	def get_queryset(self):
		user = self.request.user
		queryset = CustomerProfile.objects.all().order_by('-created_at')
		return queryset.filter(company__auth_user=user.id)


class ActiveCustomer(ListAPIView):
	"""
	User listing GET API
	
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Active user within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = UserlistingSerializer
	def get_queryset(self):
		user = self.request.user
		queryset = CustomerProfile.objects.filter(active_status=1).order_by('-created_at')
		return queryset.filter(company__auth_user=user.id)







