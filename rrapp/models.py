from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import desc

db = SQLAlchemy()

class FareType(db.Model):
    """
    Table that stores types of fares
    """
    __tablename__ = 'fare_types'
    fare_id = db.Column(db.Integer, nullable=False, primary_key = True, autoincrement=True)
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
    passenger_id = db.Column(db.Integer, nullable=False, primary_key = True, autoincrement=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    preferred_card_number = db.Column(db.String(16))
    preferred_billing_address = db.Column(db.String(100))
    
    

    def __init__(self,fname,lname,email,password,preferred_card_number,preferred_billing_address):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.preferred_card_number = preferred_card_number
        self.preferred_billing_address = preferred_billing_address


class Reservation(db.Model):
    """
    Table that stores reservations
    """
    __tablename__ = 'reservations'
    reservation_id = db.Column(db.Integer, nullable=False, primary_key = True, autoincrement=True)
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
    Table that stores reservations
    """
    __tablename__ = 'seats_free'
    train_id = db.Column(db.Integer, nullable=False, primary_key = True, db.ForeignKey('trains.train_id'))
    segment_id = db.Column(db.Integer, nullable=False, primary_key = True, db.ForeignKey('segments.segment_id'))
    seat_free_date = db.Column(db.Date, nullable=False)
    freeseat = db.Column(db.Integer, nullable=False, default=448)
    
    

    def __init__(self,train_id,segment_id,seat_free_date,billing_address):
        self.reservation_date = reservation_date
        self.paying_passenger_id = paying_passenger_id
        self.card_number = card_number
        self.billing_address = billing_address

class Segment(db.Model):
    """
    Table that stores reservations
    """
    __tablename__ = 'segments'
    segment_id = db.Column(db.Integer, nullable=False, primary_key = True, autoincrement=True)
    seg_n_end = db.Column(db.Integer, nullable=False, db.ForeignKey('stations.station_id'))
    seg_s_end = db.Column(db.Integer, nullable=False, db.ForeignKey('stations.station_id'))
    seg_fare = db.Column(db.Numeric(7,2), nullable=False)

    def __init__(self,seg_n_end,seg_s_end,seg_fare):
        self.seg_n_end = reservation_date
        self.seg_s_end = paying_passenger_id
        self.seg_fare = card_number


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
    train_id = db.Column(db.Integer, nullable=False, primary_key=True, db.ForeignKey('trains.train_id'))
    station_id = db.Column(db.Integer, nullable=False, primary_key=True, db.ForeignKey('stations.station_id'))
    time_in = db.Column(db.Time)
    time_out = db.Column(db.Time)

    def __init__(self, train_id, station_id, time_in, time_out):
        self.train_id = train_id
        self.station_id = station_id
        self.time_in = time_in
        self.time_out = time_out

