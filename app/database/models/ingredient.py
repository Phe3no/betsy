from peewee import Model, CharField, BooleanField
from flask import current_app
from ..db import get_db

with current_app.app_context():
    db = get_db()


class Ingredient(Model):
    name = CharField(unique=True)
    is_vegetarian = BooleanField()
    is_vegan = BooleanField()
    is_glutenfree = BooleanField()

    class Meta:
        database = db
