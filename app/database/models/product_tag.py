from peewee import Model, ForeignKeyField, CompositeKey
from .product import Product
from .tag import Tag
from flask import current_app
from ..db import get_db

with current_app.app_context():
    db = get_db()


class ProductTag(Model):
    product_id = ForeignKeyField(Product, column_name='prid')
    tag_id = ForeignKeyField(Tag, column_name='taid')

    class Meta:
        database = db
        primary_key = CompositeKey("product_id", "tag_id")