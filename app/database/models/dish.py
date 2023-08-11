from peewee import Model, TextField, ForeignKeyField, IntegerField, ManyToManyField
from .restaurant import Restaurant
from .ingredient import Ingredient
from flask import current_app
from ..db import get_db

with current_app.app_context():
    db = get_db()


class Dish(Model):
    name = TextField(unique=True)
    served_at = ForeignKeyField(Restaurant)
    price_in_cents = IntegerField()
    ingredients = ManyToManyField(Ingredient, backref="composition")

    class Meta:
        database = db
