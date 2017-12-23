from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import TextAreaField, DateTimeField, IntegerField, FileField, ValidationError, FieldList
from wtforms.validators import DataRequired, Email, Length
from .models import Passenger
from datetime import datetime

def validate_email(form,field):
	if not Passenger.is_unique_email(field.data):
		raise ValidationError('There already exists an account with this email.')
		return False
	return True

class SignupForm(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired('Please enter your first name.')])
	last_name = StringField('Last name', validators=[DataRequired('Please enter your last name.')])
	email = StringField('Email', validators=[DataRequired('Please enter your email.'), Email('Please enter a valid email.'), validate_email])
	password = PasswordField('Password', validators=[DataRequired('Please enter a password.'), Length(min=6, message='Passwords must have at least 6 characters.')])
	confirm_password = PasswordField(label='Confirm Password', id ='confirm_password', validators=[DataRequired('Please confirm your password.')])
	credit_card = StringField(label='Credit Card Number', id='credit_card', validators=[DataRequired('Please enter the credit card number.'), Length(min=16, message='Please type a valid credit card number.')])
	billing_address = StringField(label='Billing Address', id='billing_address', validators=[DataRequired('Please enter the billing address.')])
	submit = SubmitField('Sign in')
	
class LoginForm(FlaskForm):
	email = StringField(label='Email', id='email', validators=[DataRequired('Please enter your email.')])
	password = PasswordField(label='Password', id='password', validators=[DataRequired('Please enter your password.')])
	submit = SubmitField('Sign in')



