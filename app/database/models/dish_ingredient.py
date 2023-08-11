from peewee import Model, CharField
from flask import current_app

from ..db import get_db

with current_app.app_context():
    db = get_db()


class DishIngredient(Model):
    dish_id = CharField()
    ingredient = CharField()

    class Meta:
        database = db