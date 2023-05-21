from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect('/user/login')


@app.route('/user/login')
def login():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')


@app.route('/user/login/process', methods=['POST'])
def login_success():
    user = User.verify_login(request.form)
    if not user:
        return redirect('/user/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/user/register/process', methods=['POST'])
def register():
    if not User.verify_register(request.form):
        return redirect('/')

    print(request.form)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')


@app.route('/user/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/user/login')