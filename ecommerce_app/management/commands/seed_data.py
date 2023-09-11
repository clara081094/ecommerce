from django.core.management.base import BaseCommand
from ...models import Category, Product, User, Promotion

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        data_category = [
            {'name': 'Coffee', 'description': 'All kinds of coffee seeds'},
            {'name': 'Equipment', 'description': 'Items, tools, machinery, or devices that perform specific functions, operations, or processes'},
            {'name': 'Accesories', 'description': 'Items or additional components that are used to complement, enhance, or extend a functionality'},
        ]
        data_products = [
            {'name': 'Liberica', 'price': '2.53','category_id':1},
            {'name': 'Arabica', 'price': '1.43','category_id':1},
            {'name': 'Personal Computer', 'price': '220','category_id':2},
            {'name': 'TypeWriter', 'price': '80.45','category_id':2},
            {'name': 'Airpods', 'price': '100.34','category_id':3},
            {'name': 'iWatch', 'price': '120.23','category_id':3},
        ]
        data_promotions = [
            {'category_id':1,'element':'unit','element_min':1,'benefit':'unit','benefit_qnt':1},
            {'category_id':2,'element':'unit','element_min':3,'benefit':'shipping','benefit_qnt':0},
            {'category_id':3,'element':'dollar','element_min':70,'benefit':'discount','benefit_qnt':10},
        ] 

        data_users = [
            {'user_code': 'USR_1', 'full_name': 'John Smith', 'email':'test_user@testdomain.com'}
        ]

        for item in data_category:
            Category.objects.create(**item)
        for item in data_products:
            Product.objects.create(**item)
        for item in data_users:
            User.objects.create(**item)
        for item in data_promotions:
            Promotion.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Data seeded successfully'))