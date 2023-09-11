import json
from django.db.models import Sum, F

from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    CartDataSerializer, 
    CartItemSerializer,
    CartEditSerializer,
    CartSerializer,
    OrderCreateSerializer,
    OrderSerializer
)
from ..models import (
    Cart, 
    User, 
    Product, 
    Promotion, 
    ProductCart, 
    Order
)
from ..exceptions import ExceptionParams

@api_view(["POST"])
def cart(request):
    cart_serializer = CartDataSerializer(data=request.data)
    if cart_serializer.is_valid():
        existing_user = User.objects.filter(user_code = request.data.get('user_code')).first()
        if not existing_user:
            raise ExceptionParams(errors = "User not found", status_code=400)
        existing_cart = Cart.objects.filter(user = existing_user).first()
        if not existing_cart:
            new_cart = Cart(user = existing_user)
            new_cart.save()
            return Response(CartSerializer(new_cart).data, status=status.HTTP_201_CREATED)
        else:
            raise ExceptionParams(errors = "Cart already exists", status_code=400)
    raise ExceptionParams(errors = cart_serializer.errors)

@api_view(["GET"])
def get_cart(request, cart_id):
    existing_cart = Cart.objects.filter(id = cart_id).first()
    if not existing_cart:
        raise ExceptionParams(errors = "Cart not found", status_code=400)
    return Response(CartSerializer(existing_cart).data, status=status.HTTP_200_OK)

@api_view(["POST"])
def add_item_to_cart(request, cart_id):

    existing_cart = Cart.objects.filter(id = cart_id).first()
    if not existing_cart:
        raise ExceptionParams(errors = "Cart not found", status_code=400)
    
    product_id = request.data.get('product_id')
    existing_product = Product.objects.filter(id = product_id).first()
    if not existing_product:
        raise ExceptionParams(errors = "Product not found", status_code=400)
    
    qnt = 1 if request.data.get('quantity') is None else request.data.get('quantity')

    cart_product = ProductCart(cart= existing_cart,product=existing_product)
    cart_product.quantity = qnt
    cart_product.save()

    return Response(CartItemSerializer(cart_product).data, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
def update_cart_item_quantity(request, cart_id, product_id):

    cart_serializer = CartEditSerializer(data=request.data)
    if cart_serializer.is_valid():
        new_quantity = request.data.get('quantity')

        existing_cart = Cart.objects.filter(id = cart_id).first()
        if not existing_cart:
            raise ExceptionParams(errors = "Cart not found", status_code=400)
        
        existing_product = ProductCart.objects.filter(id = product_id).first()
        if not existing_product:
            raise ExceptionParams(errors = "Product not found in cart", status_code=400)
        
        cart_product = ProductCart.objects.filter(cart = existing_cart,product = existing_product).first()
        cart_product.quantity += new_quantity
        cart_product.save()
        return Response(CartItemSerializer(cart_product).data, status=status.HTTP_201_CREATED)
        
    else:
        raise ExceptionParams(errors= cart_serializer.errors)

@api_view(["POST"])
def order(request):

    if request.method == "POST":

        order_serializer = OrderCreateSerializer(data=request.data)
        if order_serializer.is_valid():
            
            existing_cart = Cart.objects.filter(id = request.data.get('cart_id')).first()
            if not existing_cart:
                return ExceptionParams(errors = "Cart not found", status=status.HTTP_400_BAD_REQUEST)
            
            cart_categories = set()
            for cart_item in existing_cart.productcart_set.all():
                cart_categories.add(cart_item.product.category.id)

            list_cart_categories = list(cart_categories)
            if len(list_cart_categories) <= 0 :
                raise ExceptionParams(errors = "Cart is empty", status_code=400)
            
            #In the absence of shipping conditionals, I implement a fixed shipping cost.
            total_shipping = 5 

            total_amount = 0
            total_discount = 0
            total_number_products = 0

            for cart_category in list_cart_categories:
                total_discount_category = 0
                promotion = Promotion.objects.filter(category__id = cart_category).first()
                total_amount_category = ProductCart.objects.filter(cart=existing_cart, product__category__id=cart_category).\
                    values().annotate(total_amount=Sum(F('quantity') * F('product__price'))).first()
                total_qnt_category = ProductCart.objects.filter(cart=existing_cart, product__category__id=cart_category).\
                    values().annotate(total_amount=Sum(F('quantity'))).first()
                
                total_qnt_category = total_qnt_category.get('total_amount')
                total_amount_category = total_amount_category.get('total_amount')
  
                if (promotion.element == 'unit'):
                    relative_total = total_qnt_category
                if (promotion.element == 'dollar'):
                    relative_total = total_amount_category

                if (relative_total > promotion.element_min) :
                    if (promotion.benefit == 'unit'):
                        cart_product = ProductCart.objects.filter(cart=existing_cart, product__category__id=cart_category).first()
                        cart_product.quantity += 1
                        cart_product.save()
                        total_qnt_category += 1
                    if (promotion.benefit == 'shipping'):
                        total_shipping = 0
                    if (promotion.benefit == 'discount'):
                        total_discount_category = total_amount_category*promotion.benefit_qnt /100

                total_amount += ( total_amount_category - total_discount_category)
                total_discount += total_discount_category
                total_number_products += total_qnt_category
                
            new_order = Order(
                cart = existing_cart,
                total_product = total_number_products,
                total_discount = total_discount,
                total_shipping = total_shipping,
                total_order = total_amount - total_shipping
            )

            return Response(OrderSerializer(new_order).data, status=status.HTTP_201_CREATED)
        raise ExceptionParams(order_serializer.errors, status_code=400)