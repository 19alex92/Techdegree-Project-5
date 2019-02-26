from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField,
                     IntegerField, DateTimeField)
from wtforms.validators import DataRequired


class Entry(Form):
    title = StringField("What is the title", validators=[DataRequired()])
    date = DateTimeField("What is the date?", validators=[DataRequired()])
    time_spent = IntegerField("How much time did it take?", validators=[DataRequired()])
    learned = TextAreaField("What have you learned?", validators=[DataRequired()])
    resources = TextAreaField("What resources?", validators=[DataRequired()])
    tags = TextAreaField("What are the tags?", validators=[DataRequired()])
