from peewee import Model, AutoField, ForeignKeyField, IntegerField
from .product import Product
from .user import User
from flask import current_app
from ..db import get_db

with current_app.app_context():
    db = get_db()


class Transaction(Model):
    trid = AutoField
    product_id = ForeignKeyField(Product, column_name='prid')
    user_id = ForeignKeyField(User, column_name='us_id')
    quantity = IntegerField()

    class Meta:
        database = db