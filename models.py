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

    #@classmethod
    #def create_entry(cls, title, date, time_spent, learned, resources, tags):
    #    cls.create(
    #        title=title,
    #        date=date,
    #        time_spent=time_spent,
    #        learned=learned,
    #        resources=resources,
    #        tags=tags
    #    )

    #@classmethod
    #def test_entry(cls):
    #    cls.create(title='My first journal entry',
    #               date=datetime.datetime.now(),
    #               time_spent=45, learned="I learned a lot of cool Stuff",
    #               ressources="google.com", tags="learning, python, treehouse")


class User(UserMixin, Model):
    # Database to store the user data
    username = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    # classmethod for user creation hinzufügen


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entries, User], safe=True)
    DATABASE.close()
