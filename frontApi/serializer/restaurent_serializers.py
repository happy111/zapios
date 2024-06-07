from rest_framework import serializers

from django.db.models import Count

from Outlet.models import OutletProfile



class OutletDetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = OutletProfile
		fields = '__all__'
