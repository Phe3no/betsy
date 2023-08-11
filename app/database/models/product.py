from peewee import Model, CharField, AutoField, IntegerField, DecimalField, ForeignKeyField
from .user import User
from flask import current_app
from ..db import get_db

with current_app.app_context():
    db = get_db()


class Product(Model):
    prid = AutoField
    user_id = ForeignKeyField(User, column_name='usid')
    name = CharField(unique=True)
    description = CharField(index=True)
    price_per_unit = DecimalField()
    amount_in_stock = IntegerField()

    class Meta:
        database = db
