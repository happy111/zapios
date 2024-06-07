from rest_framework import serializers
from . models import *


class UserTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserType
		fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
	class Meta:
		model = ManagerProfile
		fields = '__all__'


class ManagerProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ManagerProfile
		fields = '__all__'
