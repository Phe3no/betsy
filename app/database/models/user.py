from peewee import Model, CharField, AutoField, TextField
from flask import current_app
from ..db import get_db

with current_app.app_context():
    db = get_db()


class User(Model):
    us_id = AutoField
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    address_data = TextField()
    billing_information = CharField()

    class Meta:
        database = db
