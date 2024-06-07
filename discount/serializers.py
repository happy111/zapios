from rest_framework import serializers
from . models import *
from datetime import datetime, timedelta


class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupon
		fields = '__all__'

class QuantityComboSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		print("dddddddddddddddddd")
		representation = super(QuantityComboSerializer, self).to_representation(instance)
		if instance.product != None:
			representation['product_name'] = Product.objects.filter(id=instance.product_id)[0].product_name
		else:
			representation['product_name'] = ''
		return representation

	class Meta:
		model = QuantityCombo
		fields = '__all__'

class PercentComboSerializer(serializers.ModelSerializer):
	class Meta:
		model = PercentCombo
		fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Discount
		fields = '__all__'



class CouponsSerializer(serializers.ModelSerializer):
	# category_name = serializers.ReadOnlyField(source = 'category.category_name')

	def to_representation(self, instance):
		representation = super(CouponsSerializer, self).to_representation(instance)


		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		if instance.valid_frm !=None:
			v_time = instance.valid_frm+timedelta(hours=5,minutes=30)
			representation['valid_frm'] = v_time.strftime("%d/%b/%y")
		else:
			pass
		if instance.valid_till !=None:
			v_till = instance.valid_frm+timedelta(hours=5,minutes=30)
			representation['valid_till'] = v_till.strftime("%d/%b/%y")
		else:
			pass
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = Discount
		fields = ['id',
				  'discount_type',
				  'discount_name',
				  'valid_frm',
				  'valid_till',
				  'active_status']


class ReasonSerializer(serializers.ModelSerializer):
	class Meta:
		model = DiscountReason
		fields = '__all__'
