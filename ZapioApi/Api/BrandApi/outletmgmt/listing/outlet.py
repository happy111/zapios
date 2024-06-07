from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
from Outlet.models import OutletProfile

#Serializer for api
from rest_framework import serializers
from UserRole.models import ManagerProfile


class OutletSerializer(serializers.ModelSerializer):
	# company_name = serializers.ReadOnlyField(source='Company.company_name')
	class Meta:
		model = OutletProfile
		fields = ['id','Outletname','is_open','opening_time','closing_time']
	
	def to_representation(self, instance):
		representation = super(OutletSerializer, self).to_representation(instance)
				
		if instance.opening_time != None:
			representation['opening_time'] = instance.opening_time.strftime("%I:%M %p")
		else:
			pass
		if instance.closing_time != None:
			representation['closing_time'] = instance.closing_time.strftime("%I:%M %p")
		else:
			pass
		return representation

class OutletIdNamelisting(ListAPIView):
	"""
	Active Outlet listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Active limited Outlet data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = OutletSerializer

	def get_queryset(self):
		user = self.request.user.id
		ch_brand = Company.objects.filter(auth_user_id=user)
		if ch_brand.count() > 0:
			nuser=user
		else:
			pass
		ch_cashier = ManagerProfile.objects.filter(auth_user_id=user)
		if ch_cashier.count() > 0:
			company_id = ch_cashier[0].Company_id
			auth_user_id = Company.objects.filter(id=company_id)[0].auth_user_id
			nuser=auth_user_id
		else:
			pass
		queryset = OutletProfile.objects.filter(active_status=1,is_hide=0).order_by('-created_at')
		return queryset.filter(Company__auth_user=nuser)