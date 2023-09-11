from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from ..models import Cart, ProductCart, Product, User, Category

class CartProductAddItemToCartTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create(
            user_code='USR_2',
            full_name='testuser',
            email='testemail@testdomain.com'
        )

        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name='Category 1', description ='Description for category 1')
        self.product = Product.objects.create(name='Product 1', price=10.0, category = self.category)
        self.client = APIClient()

    def test_add_item_to_cart(self):

        url = reverse('add_item_to_cart', kwargs={'cart_id': self.cart.id})
        data = {"quantity": 4, "product_id": self.product.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductCart.objects.count(), 1)
        cart_item = ProductCart.objects.first()
        self.assertEqual(cart_item.quantity, 4)
        
        # Check that the product name is correct
        self.assertEqual(response.data.get('product')['name'], 'Product 1')