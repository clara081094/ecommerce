from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=400)

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class User(models.Model):
    user_code = models.CharField(max_length=10)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length = 50)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="ProductCart")

class ProductCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Promotion(models.Model):
    ELEMENT_CHOICES = (
        ('unit', 'unit'),
        ('dollar', 'dollar'),
    )
    BENEFIT_CHOICES = (
        ('unit', 'unit'),
        ('free_shipping', 'free_shipping'),
        ('discount', 'discount'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    element = models.CharField(max_length = 20, choices=ELEMENT_CHOICES)
    element_min = models.IntegerField()
    benefit = models.CharField(max_length = 20, choices=BENEFIT_CHOICES)
    benefit_qnt = models.DecimalField(max_digits=8, decimal_places=2)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_product = models.FloatField()
    total_discount = models.FloatField()
    total_shipping = models.FloatField()
    total_order = models.FloatField()