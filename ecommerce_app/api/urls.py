from django.urls import path
from . import views

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("cart/<cart_id>", views.get_cart, name="get_cart"),
    path('cart/<cart_id>/product', views.add_item_to_cart, name='add_item_to_cart'),
    path('cart/<cart_id>/product/<int:product_id>', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path("order", views.order, name="order"),
]