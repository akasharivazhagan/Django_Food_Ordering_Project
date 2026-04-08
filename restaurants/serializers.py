from rest_framework import serializers
from .models import Restaurant, Food

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'