from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from restaurants.models import Food


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


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