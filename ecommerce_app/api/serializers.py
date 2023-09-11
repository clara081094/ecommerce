from rest_framework import serializers
from ..models import Cart, ProductCart, Order, Product

class CartDataSerializer(serializers.Serializer):
    user_code = serializers.CharField(max_length=10)

class CartEditSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category_id')

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductCart
        fields = ('id', 'product', 'quantity')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'products')

class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    class Meta:
        model = Order
        fields = ('id', 'cart', 'total_product','total_discount','total_shipping','total_order')

