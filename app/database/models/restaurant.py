from peewee import Model, CharField, DateTimeField, TimeField
from flask import current_app
from ..db import get_db

with current_app.app_context():
    db = get_db()


class Restaurant(Model):
    name = CharField()
    open_since = DateTimeField()
    opening_time = TimeField()
    closing_time = TimeField()

    class Meta:
        database = db
