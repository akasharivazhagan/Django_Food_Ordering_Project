from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from restaurants.models import Food


class CartItemSerializer(serializers.ModelSerializer):
    food = serializers.CharField(source='food.name')

    class Meta:
        model = CartItem
        fields = ['food', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source='id')
    restaurant = serializers.CharField(source='restaurant.name')
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['cart_id', 'restaurant', 'items']


class AddToCartSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    
        
class AddToCartResponseSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    food = serializers.CharField()
    quantity = serializers.IntegerField()