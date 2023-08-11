from peewee import Model, AutoField, CharField
from .product import Product
from .user import User
from flask import current_app
from ..db import get_db

with current_app.app_context():
    db = get_db()


class Tag(Model):
    taid = AutoField()
    tag = CharField()

    class Meta:
        database = db