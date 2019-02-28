import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')


class Entries(Model):
    # Database to store the entries
    title = CharField(max_length=250)
    date = DateTimeField()
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()
    tags = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                )
        except IntegrityError:
            raise ValueError("User already exists")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entries, User], safe=True)
    DATABASE.close()
