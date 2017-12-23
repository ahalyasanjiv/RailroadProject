from sqlalchemy.sql.expression import func
from flask import flash, render_template, request, session, redirect, url_for
from rrapp import app
from .forms import SignupForm, LoginForm, ReservationForm
from .models import db, Passenger, SeatsFree, Segment, Trips, Trains, Reservation, Station
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

@app.route('/reserve', methods=["GET", "POST"])
def reserve():
    def get_station_choices():
        stationList = Station.get_all_stations()
        stations = []
        for station in stationList:
            value = station.station_id
            label = station.station_name

            stations.append((value,label))

        return stations

    form = ReservationForm()

    if request.method == "GET":
        return render_template("reserve.html",form=form)
    elif request.method == "POST":
        start = form.start_station.data
        end = form.end_station.data
        date= form.date.data

        return redirect(url_for('chooseTrip', start_station=start, end_station=end, trip_date=date))


@app.route('/choosetrip/<start_station>/<end_station>/<trip_date>', methods=['GET','POST'])
def chooseTrip(start_station,end_station,trip_date):
    if 'user' not in session:
        return redirect(url_for('index'))
    available_trains = Trains.get_available_trains(int(start_station),int(end_station),trip_date)
    if request.method ==  'GET':
        return render_template('choosetrip.html',available_trains=available_trains,start_station=start_station, end_station=end_station, trip_date=trip_date)
    else:
        if request.form['train'] != '-1':
            session['trip_info'] = {'start_station':start_station,'end_station':end_station,'train_id':request.form['train'],'trip_date':trip_date}
            return redirect(url_for('confirmReservation'))
        else:
            flash('Please select a train.')
            return render_template('choosetrip.html',available_trains=available_trains,start_station=start_station, end_station=end_station, trip_date=trip_date)

@app.route('/confirmreservation', methods=['GET','POST'])
def confirmReservation():
    if 'user' not in session or 'trip_info' not in session:
        return redirect(url_for('index'))
    start_station = session['trip_info']['start_station']
    end_station = session['trip_info']['end_station']
    train_id = session['trip_info']['train_id']
    total_fare = Trips.get_trip_fare(start_station,end_station)
    trip_date = session['trip_info']['trip_date']
    time_in = str(Trains.get_train_time_in(train_id,start_station))
    time_out = str(Trains.get_train_time_out(train_id,end_station))
    trip_info = {'start_station':start_station, 'end_station':end_station, 'train_id':train_id, 'trip_date':trip_date, 'time_in':time_in, 'time_out':time_out, 'total_fare':total_fare}
    if request.method == 'GET':
        return render_template('confirmreservation.html',trip_info=trip_info)
    else:
        passenger_info = Passenger.get_passenger_info(session['user'])
        reservation_date = func.now()
        newReservation = Reservation(reservation_date, passenger_info['passenger_id'], passenger_info['card_number'], passenger_info['billing_address'])
        db.session.add(newReservation)
        reservation_id = Reservation.get_reservation_id(reservation_date, passenger_info['passenger_id'])
        newTrip = Trips(trip_date, start_station, end_station, 1, total_fare, int(train_id), reservation_id)
        db.session.add(newTrip)
        db.session.commit()
        session.pop('trip_info', None)
        return redirect(url_for('index'))
    
@app.route('/viewreservations', methods=['GET','POST'])
def viewReservations():
    if 'user' not in session:
        return render_template('index.html')
    elif request.method == "POST":
        #Modify reservation
        if request.form["action"] == "Modify":
            return redirect(url_for("modifyReservation"))
        #Cancel Reservation
        elif request.form["action"] == "Cancel":
            return redirect(url_for("cancelReservation")) 
    else:
        passenger_info = Passenger.get_passenger_info(session['user'])
        reservations = Reservation.get_passenger_reservations(passenger_info['passenger_id'])
        trip_info = {}
        for reservation in reservations:
            trip_info[reservation["reservation_id"]] = Trips.get_trip_info_from_reservation_id(reservation["reservation_id"])
        return render_template('viewreservations.html', reservations=reservations, trip_info=trip_info)

@app.route("/modifyreservation", methods=["GET", "POST"])
def modifyReservation():
    return render_template("index.html")

@app.route("/cancelreservation", methods=["GET", "POST"])
def cancelReservation():
    return render_template("index.html")
    if 'user' not in session:
        return render_template('index.html')
    else:
        passenger_info = Passenger.get_passenger_info(session['user'])
        reservations = Reservation.get_passenger_reservations(passenger_info['passenger_id'])
        trip_info = {}
        for reservation in reservations:
            trip_info[reservation["reservation_id"]] = Trips.get_trip_info_from_reservation_id(reservation["reservation_id"])
        return render_template('viewreservations.html', reservations=reservations, trip_info=trip_info)
