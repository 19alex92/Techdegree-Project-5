from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField,
                     IntegerField, SubmitField)
from wtforms.validators import (DataRequired, ValidationError,
                                Email, Length, EqualTo
                                )
from wtforms.fields.html5 import DateField

from models import User


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
    register = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')


class EntryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    time_spent = IntegerField("Time Spent",
                              validators=[
                                  DataRequired(message='This field is required'
                                                       ' and must be a number')
                                  ])
    learned = TextAreaField("What I Learned", validators=[DataRequired()])
    resources = TextAreaField("Resources to Remember",
                              validators=[DataRequired()])
    tags = TextAreaField("Tags")
    submit = SubmitField('Publish Entry')
