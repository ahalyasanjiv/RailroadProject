from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import desc
from werkzeug import generate_password_hash, check_password_hash
from flask import session

db = SQLAlchemy()

class FareType(db.Model):
    """
    Table that stores types of fares
    """
    __tablename__ = 'fare_types'
    fare_id = db.Column(db.Integer, nullable=False, primary_key = True)
    fare_name = db.Column(db.String(20))
    rate = db.Column(db.Numeric(3,2))
    

    def __init__(self,judge_id,entry_id,vocals):
        self.judge_id = judge_id
        self.entry_id = entry_id
        self.vocals = vocals

class Passenger(db.Model):
    """
    Table that stores passengers
    """
    __tablename__ = 'passengers'
    passenger_id = db.Column(db.Integer, nullable=False, primary_key = True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100))
    preferred_card_number = db.Column(db.String(16))
    preferred_billing_address = db.Column(db.String(100))
    
    

    def __init__(self,fname,lname,email,password,preferred_card_number,preferred_billing_address):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = generate_password_hash(password)
        self.preferred_card_number = preferred_card_number
        self.preferred_billing_address = preferred_billing_address

    def check_password(self, password):
        return check_password_hash(self.password,password)

    @staticmethod
    def is_unique_email(email):
    	if db.session.query(Passenger.passenger_id).filter(Passenger.email==email).count() > 0:
    		return False
    	return True


class Reservation(db.Model):
    """
    Table that stores reservations
    """
    __tablename__ = 'reservations'
    reservation_id = db.Column(db.Integer, nullable=False, primary_key = True)
    reservation_date = db.Column(db.DateTime(timezone=False), default=func.now())
    paying_passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id'), nullable=False)
    card_number = db.Column(db.String(16))
    billing_address = db.Column(db.String(100))
    
    

    def __init__(self,reservation_date,paying_passenger_id,card_number,billing_address):
        self.reservation_date = reservation_date
        self.paying_passenger_id = paying_passenger_id
        self.card_number = card_number
        self.billing_address = billing_address

class SeatsFree(db.Model):
    """
    Table that stores seatsFree
    """
    __tablename__ = 'seats_free'
    train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id'), nullable=False, primary_key = True)
    segment_id = db.Column(db.Integer, db.ForeignKey('segments.segment_id'), nullable=False, primary_key = True)
    seat_free_date = db.Column(db.Date, nullable=False)
    freeseat = db.Column(db.Integer, nullable=False, default=448)
    
    

    def __init__(self,train_id,segment_id,seat_free_date,freeseat):
        self.train_id = train_id
        self.segment_id = segment_id
        self.seat_free_date = seat_free_date
        self.freeseat = freeseat


class Segment(db.Model):
    """
    Table that stores segments
    """
    __tablename__ = 'segments'
    segment_id = db.Column(db.Integer, nullable=False, primary_key = True)
    seg_n_end = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    seg_s_end = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    seg_fare = db.Column(db.Numeric(7,2), nullable=False)

    def __init__(self,seg_n_end,seg_s_end,seg_fare):
        self.seg_n_end = seg_n_end
        self.seg_s_end = seg_s_end
        self.seg_fare = seg_fare

    @staticmethod
    def get_segment(seg_n_end):
    	segment = db.session.query(Segment.segment_id).filter_by(seg_n_end = seg_n_end).first()[0]
    	return segment

class Trains(db.Model):
    """
    Table that stores trains
    """
    __tablename__ = "trains"
    train_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    train_start = db.Column(db.Integer, db.ForeignKey("stations.station_id"), nullable=False)
    train_end = db.Column(db.Integer, db.ForeignKey("stations.station_id"), nullable=False)
    train_direction = db.Column(db.Integer, default=None)
    train_days = db.Column(db.Integer, default=None)

    def __init__(self, train_start, train_end, train_direction, train_days):
        self.train_start = train_start
        self.train_end = train_end
        self.train_direction = train_direction
        self.train_days = train_days

    @staticmethod
    def get_all_train_ids():
    	trains_query = db.session.query(Trains.train_id).all()
    	trains = []
    	for train in trains_query:
    		trains.append(train[0])
    	trains.sort()
    	return trains

    @staticmethod
    def is_train_free_for_trip(train_id,start_station,end_station,seat_free_date):
    	# if direction of trip does not match train direction, return False
    	direction = Trips.get_trip_direction(start_station,end_station)
    	train_direction = db.session.query(Trains.train_direction).filter_by(train_id = train_id).first()
    	if train_direction:
    		if direction != train_direction[0]:
    			return False
    	if not train_direction:
    		return False
    	# if northbound, set start_station to seg_n_end and end_station to seg_s_end
    	if direction == 1:
    		seg_n_end = start_station
    		seg_s_end = end_station
    	# else, flip it
    	else:
    		seg_n_end = end_station
    		seg_s_end = start_station
    	# check if train is in seats_free table
    	if db.session.query(SeatsFree).filter_by(train_id = train_id, seat_free_date=seat_free_date).count() == 0:
    		return False
    	# for every segment between seg_n_end and seg_s_end:
    	for i in range(seg_n_end,seg_s_end):
    		# query the segments table to get the segment id of that segment
    		segment = Segment.get_segment(i)
    		# check if there is at least 1 empty seat for that trip
    		if db.session.query(SeatsFree.freeseat).filter_by(train_id = train_id, segment_id = segment, seat_free_date = seat_free_date).first()[0] < 1:
    			return False
    	# return True
    	return True

    @staticmethod
    def get_available_trains(start_station,end_station,seat_free_date):
        trains = Trains.get_all_train_ids()
        available_trains = []
        for train_id in trains:
            if Trains.is_train_free_for_trip(train_id,start_station,end_station,seat_free_date):
                time_in = str(Trains.get_train_time_in(train_id,start_station))
                time_out = str(Trains.get_train_time_out(train_id,end_station))
                total_fare = Trips.get_trip_fare(start_station,end_station)
                available_trains.append({'train_id':train_id,'time_in':time_in,'time_out':time_out,'total_fare':total_fare})
        return available_trains
    @staticmethod
    def get_train_time_in(train_id, station_id):
        time_in = db.session.query(StopsAt.time_in).filter_by(train_id = train_id, station_id=station_id).first()[0]
        return time_in

    @staticmethod
    def get_train_time_out(train_id, station_id):
        time_out = db.session.query(StopsAt.time_out).filter_by(train_id = train_id, station_id=station_id).first()[0]
        return time_out

class Trips(db.Model):
    """
    Table that stores trips
    """
    __tablename__ = "trips"
    trip_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    trip_date = db.Column(db.Date, nullable=False)
    trip_seg_start = db.Column(db.Integer, db.ForeignKey("segments.segment_id"), nullable=False)
    trip_seg_ends = db.Column(db.Integer, db.ForeignKey("segments.segment_id"), nullable=False)
    fare_type = db.Column(db.Integer, db.ForeignKey("fare_types.fare_id"), nullable=False)
    fare = db.Column(db.Numeric(7,2), nullable=False)
    trip_train_id = db.Column(db.Integer, db.ForeignKey("trains.train_id"), nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.reservation_id"), nullable=False)

    def __init__(self, trip_date, trip_seg_start, trip_seg_ends, fare_type, fare, trip_train_id, reservation_id):
        self.trip_date = trip_date
        self.trip_seg_start = trip_seg_start
        self.trip_seg_ends = trip_seg_ends
        self.fare_type = fare_type
        self.fare = fare
        self.trip_train_id = trip_train_id
        self.reservation_id = reservation_id

    @staticmethod
    def get_trip_direction(start_station,end_station):
    	if start_station > end_station:
    		return 0
    	elif end_station > start_station:
    		return 1

    @staticmethod
    def get_trip_fare(start_station,end_station):
        if start_station > end_station:
            seg_n_end = end_station
            seg_s_end = start_station
        else:
            seg_n_end = start_station
            seg_s_end = end_station
        total_fare = 0
        for i in range(seg_n_end,seg_s_end):
            seg_fare = db.session.query(Segment.seg_fare).filter_by(segment_id = i).first()[0]
            total_fare += seg_fare
        return total_fare


class Station(db.Model):
    """
    Table that stores stations.
    """
    __tablename__ = 'stations'
    station_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    station_name = db.Column(db.String(40), nullable=False)
    station_symbol = db.Column(db.String(3), nullable=False, unique=True)

    def __init__(self, station_name, station_symbol):
        self.station_name = station_name
        self.station_symbol = station_symbol



class StopsAt(db.Model):
    """
    Stops at table.
    """

    __tablename__= 'stops_at'
    train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id'), nullable=False, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False, primary_key=True)
    time_in = db.Column(db.Time)
    time_out = db.Column(db.Time)

    def __init__(self, train_id, station_id, time_in, time_out):
        self.train_id = train_id
        self.station_id = station_id
        self.time_in = time_in
        self.time_out = time_out

