import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('adogtame.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    
    class Meta:
        database = DATABASE


class Dog(Model):
    name = CharField()
    age = IntegerField()
    breed = CharField()
    personality = CharField()
    city = CharField()
    vaccines = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Article(Model):
    title = CharField(max_length=200)
    summary = TextField()
    body = TextField()
    image = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE


class Veterinarian(Model):
    name = CharField()
    address = CharField()
    city = CharField()
    phone = CharField()
    email = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE


class Tip(Model):
    tip = CharField(max_length=200)
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog, User, Veterinarian, Article, Tip], safe=True)
    print("TABLES Created")
    DATABASE.close()