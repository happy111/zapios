from rest_framework import serializers
from . models import *




class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = '__all__'



class FoodTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = FoodType
		fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variant
		fields = '__all__'


class AddonDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddonDetails
		fields = '__all__'


class ProductsubCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductsubCategory
		fields = '__all__'








class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'

class FoodTypelistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = FoodType
		fields = '__all__'


class AddonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Addons
		fields = '__all__'



class SubCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductsubCategory
		fields = '__all__'



class AddonsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Addons
		fields = '__all__'




class AddongroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddonDetails
		fields = '__all__'