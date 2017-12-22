from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import desc
from flask import session

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
    Table that stores seatsFree
    """
    __tablename__ = 'seats_free'
    train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id'), nullable=False, primary_key = True)
    segment_id = db.Column(db.Integer, db.ForeignKey('segments.segment_id'), nullable=False, primary_key = True)
    seat_free_date = db.Column(db.Date, nullable=False)
    freeseat = db.Column(db.Integer, nullable=False, default=448)
    
    

    def __init__(self,train_id,segment_id,seat_free_date,billing_address):
        self.reservation_date = reservation_date
        self.paying_passenger_id = paying_passenger_id
        self.card_number = card_number
        self.billing_address = billing_address

class Segment(db.Model):
    """
    Table that stores segments
    """
    __tablename__ = 'segments'
    segment_id = db.Column(db.Integer, nullable=False, primary_key = True, autoincrement=True)
    seg_n_end = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    seg_s_end = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    seg_fare = db.Column(db.Numeric(7,2), nullable=False)

    def __init__(self,seg_n_end,seg_s_end,seg_fare):
        self.seg_n_end = seg_n_end
        self.seg_s_end = seg_s_end
        self.seg_fare = seg_fare

class Trains(db.Model):
    """
    Table that stores trains
    """
    __tablename__ = "trains"
    train_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    train_start = db.Column(db.Integer, nullable=False, db.ForeignKey("stations.station_id"))
    train_end = db.Column(db.Integer, nullable=False, db.ForeignKey("stations.station_id"))
    train_direction = db.Column(db.Integer, default=None)
    train_days = db.Column(db.Integer, default=None)

    def __init__(self, train_start, train_end, train_direction, train_days):
        self.train_start = train_start
        self.train_end = train_end
        self.train_direction = train_direction
        self.train_days = train_days



        