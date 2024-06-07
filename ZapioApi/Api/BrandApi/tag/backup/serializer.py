from rest_framework import serializers
from kitchen.models import Ingredient



class IngredientSerializer(serializers.ModelSerializer):

	class Meta:
		model = Ingredient
		fields = '__all__'
