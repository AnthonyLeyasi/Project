from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.trainers import Trainer
from flask_app import app
from flask_app.controller import user
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)