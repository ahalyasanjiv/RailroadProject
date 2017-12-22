from sqlalchemy.sql.expression import func
from flask import flash, render_template, request, session, redirect, url_for
from rrapp import app
from .forms import SignupForm, LoginForm
from .models import db
import urllib.parse
import os
import datetime

# Connect to postgresql (local to your machine)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql://postgres:1@localhost:5432/cbapp')

db.init_app(app)
app.secret_key = 'development-key'

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))
    form = SignupForm()
    if request.method == 'GET':
    	return render_template('signup.html',form=form)
