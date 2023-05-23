from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.trainers import Trainer
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return redirect('/register')


@app.route('/register')
def dashboard():
    return render_template('register.html')
