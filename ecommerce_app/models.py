from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    #category = 
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=400)

class Cart(models.Model):
    #user = 

class User(models.Model):
    user_id = models.IntegerField
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length = 50)

class Order(models.Model):