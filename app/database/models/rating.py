from peewee import Model, ForeignKeyField, CharField, IntegerField
from flask import current_app
from .restaurant import Restaurant
from ..db import get_db

with current_app.app_context():
    db = get_db()


class Rating(Model):
    restaurant = ForeignKeyField(Restaurant)
    rating = IntegerField()
    comment = CharField(null=True)

    class Meta:
        database = db
