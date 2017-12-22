"""
__init__.py
Python script that contains the app.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rrapp.models import db

app = Flask(__name__)       

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/railroad'

import rrapp.routes