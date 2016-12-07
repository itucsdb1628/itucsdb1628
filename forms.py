from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, Form, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    
    password = PasswordField('Password',[validators.DataRequired()])