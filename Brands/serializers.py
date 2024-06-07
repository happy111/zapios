from rest_framework import serializers
from .models import *
from History.models import MenuCounts

class MenuSerializer(serializers.ModelSerializer):
	class Meta:
		model = MenuCounts
		fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Page
		fields = '__all__'


class PageRetrieveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Page
		fields = "__all__"

class OutOfRangeSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutOfRange
		fields = "__all__"

class ReviewMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ReviewMaster
		fields = "__all__"