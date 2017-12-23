from sqlalchemy.sql.expression import func
from flask import flash, render_template, request, session, redirect, url_for
from rrapp import app
from .forms import SignupForm, LoginForm
from .models import db, Passenger, SeatsFree, Segment, Trips, Trains
import urllib.parse
import os
import datetime

# Connect to postgresql (local to your machine)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql://postgres:1@localhost:5432/rrapp')

db.init_app(app)
app.secret_key = 'development-key'

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('index'))

    form = SignupForm()

    if request.method == 'GET':
    	return render_template('signup.html',form=form)
    else:
   		if form.validate():
   			newuser = Passenger(form.first_name.data,form.last_name.data,form.email.data, form.password.data,form.credit_card.data,form.billing_address.data)
   			db.session.add(newuser)
   			db.session.commit()
   			session['user'] = newuser.email
   			return redirect(url_for('index'))
   		else:
   			return render_template('signup.html',form=form)

@app.route('/login/', methods=['GET','POST'])
def login():
	if 'user' in session:
		return redirect(url_for('index'))

	form = LoginForm()

	if request.method == 'GET':
		return render_template('login.html',form=form)
	else:
		if form.validate():
			email = form.email.data
			password = form.password.data
			passenger = Passenger.query.filter_by(email=email).first()
			if passenger is not None and passenger.check_password(password):
				session['user'] = email
			return redirect(url_for('index'))
		else:
			flash('Incorrect username or password.')
			return render_template('login.html',form=form)

@app.route('/logout/')
def logout():
	session.pop('user', None)
	return redirect(url_for('index'))

@app.route('/choosetrip/', methods=['GET','POST'])
def choosetrip(start_station=None,end_station=None,trip_date=None):
	start_station = 2
	end_station = 1
	trip_date = '2017-11-13'
	available_trains = Trains.get_available_trains(start_station,end_station,trip_date)
	if request.method ==  'GET':
		return render_template('choosetrip.html',available_trains=available_trains)
	else:
		if request.form['train'] != '-1':
			return render_template('choosetrip.html',available_trains=available_trains)
		else:
			flash('Please select a train.')
			return render_template('choosetrip.html',available_trains=available_trains)
    		
