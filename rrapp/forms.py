from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import TextAreaField, DateTimeField, IntegerField, FileField, ValidationError, FieldList, DateField
from wtforms.validators import DataRequired, Email, Length
from .models import db, Passenger, Station
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
	submit = SubmitField('Sign up')

class ReservationForm(FlaskForm):
	start_station = SelectField(label="Departure", id="start_station", choices=[(1, 'Boston, MA - South Station'), (2, 'Boston, MA - Back Bay Station'), (3, 'Route 128, MA'), (4, 'Providence, RI'), (5, 'Kingston, RI'), (6, 'Westerly,RI'), (7, 'Mystic, CT'), (8, 'New London, CT'), (9, 'Old Saybrook, CT'), (10, 'New Haven, CT'), (11, 'Bridgeport, CT'), (12, 'Stamford, CT'), (13, 'New Rochelle, NY'), (14, 'New York, NY - Penn Station'), (15, 'Newark, NJ'), (16, 'Newark Liberty Intl. Air., NJ'), (17, 'Metro Park, NJ'), (18, 'Trenton, NJ'), (19, 'Philadelphia, PA - 30th Street Station'), (20, 'Wilmington, DE - J.R. Biden, Jr. Station'), (21, 'Aberdeen, MD'), (22, 'Baltimore, MD - Penn Station'), (23, 'BWI Marshall Airport, MD'), (24, 'New Carrollton, MD'), (25, 'Washington, DC - Union Station')], validators=[DataRequired('Please choose a station.')])
	end_station = SelectField(label="Destination", id="end_station", choices=[(1, 'Boston, MA - South Station'), (2, 'Boston, MA - Back Bay Station'), (3, 'Route 128, MA'), (4, 'Providence, RI'), (5, 'Kingston, RI'), (6, 'Westerly,RI'), (7, 'Mystic, CT'), (8, 'New London, CT'), (9, 'Old Saybrook, CT'), (10, 'New Haven, CT'), (11, 'Bridgeport, CT'), (12, 'Stamford, CT'), (13, 'New Rochelle, NY'), (14, 'New York, NY - Penn Station'), (15, 'Newark, NJ'), (16, 'Newark Liberty Intl. Air., NJ'), (17, 'Metro Park, NJ'), (18, 'Trenton, NJ'), (19, 'Philadelphia, PA - 30th Street Station'), (20, 'Wilmington, DE - J.R. Biden, Jr. Station'), (21, 'Aberdeen, MD'), (22, 'Baltimore, MD - Penn Station'), (23, 'BWI Marshall Airport, MD'), (24, 'New Carrollton, MD'), (25, 'Washington, DC - Union Station')], validators=[DataRequired('Please choose a station.')])
	date = DateField(label="Depature Date", id="date", validators=[DataRequired('Please choose a date.')])
	submit = SubmitField("Search")
