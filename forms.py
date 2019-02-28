from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField,
                     IntegerField, SubmitField)
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class EntryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date")
    time_spent = IntegerField("Time Spent", validators=[DataRequired()])
    learned = TextAreaField("What I Learned", validators=[DataRequired()])
    resources = TextAreaField("Resources to Remember", validators=[DataRequired()])
    tags = TextAreaField("Tags", validators=[DataRequired()])
    submit = SubmitField('Publish Entry')
