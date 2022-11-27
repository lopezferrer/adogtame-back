import datetime
from peewee import *
from flask_login import UserMixin, current_user
import os
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:                         
  DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
  DATABASE = SqliteDatabase('adogtame.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    admin = BooleanField(default=False, null=False)
    
    class Meta:
        database = DATABASE


class Dog(Model):
    name = CharField()
    age = IntegerField()
    breed = CharField()
    personality = CharField()
    city = CharField()
    contact_number = CharField(max_length=11)
    vaccines = BooleanField(default=False)
    image1 = CharField(max_length=250, null=True)
    image2 = CharField(max_length=250, null=True)
    created_by = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Article(Model):
    title = CharField()
    summary = TextField()
    body = TextField()
    image = CharField()
    author = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE


class Veterinarian(Model):
    name = CharField()
    address = CharField()
    city = CharField()
    phone = CharField(max_length=11)
    email = CharField()
    created_by = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE


class Tip(Model):
    tip = CharField(max_length=280)
    author = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog, User, Veterinarian, Article, Tip], safe=True)
    print("TABLES Created")
    DATABASE.close()