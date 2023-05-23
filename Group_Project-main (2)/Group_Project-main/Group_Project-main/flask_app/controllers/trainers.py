from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models.trainer import Trainer
from flask_app.models.user import User


# you will have to edit some of this code to make it fit for what you want it to do im not sure 
# about the trainer part whatever you have in mind works for me --WCSW--


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    data = {"id": session['user_id']}
    return render_template('dashboard.html', user=User.get_by_id(data), trainers=Trainer.get_all())


@app.route('/contact.html', methods=['GET'])
def contact_page():

    return render_template('contact.html')


@app.route('/about.html', methods=['GET'])
def about_page():

    return render_template('about.html')


@app.route('/trainer/new')
def create_trainer():
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('new.html')


@app.route('/trainers/new/process', methods=['POST'])
def process_trainer():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Trainer.validate_trainer(request.form):
        return redirect('/trainers/new')
    data = {
        'user_id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'gym': request.form['gym'],
        'city': request.form['city'],
        'description': request.form['description'],
        # 'trainer': request.form['trainer'],
    }
    Trainer.save(data)
    return redirect('/dashboard')


@app.route('/trainers/<int:id>')
def view_trainer(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('view.html', trainer=Trainer. get_by_id({'id': id}))


@app.route('/trainers/edit/<int:id>')
def edit_trainer(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    data = {'id': id}
    return render_template('edit.html', trainer=Trainer.get_by_id({'id': id}))


@app.route('/trainers/edit/process/<int:id>', methods=['POST'])
def process_edit_trainer(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Trainer.validate_trainer(request.form):
        return redirect(f'/trainers/edit/{id}')

    data = {
        'id': id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'gym': request.form['gym'],
        'city': request.form['city'],
        'description': request.form['description'],
        # 'trainer': request.form['trainer'],
    }
    Trainer.update(data)
    return redirect('/dashboard')


@app.route("/trainers/delete/<int:id>")
def delete_trainer(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    data = {"id": id}
    Trainer.delete(data)
    return redirect("/dashboard")