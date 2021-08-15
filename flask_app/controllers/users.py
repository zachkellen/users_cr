from flask_app import app
from flask import render_template, request, redirect, url_for
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL


@app.route('/')
def readAll():
    users = User.get_all()
    return render_template('read.html', all_users = users)

@app.route('/create')
def createTemplate():
    return render_template('create.html')

@app.route('/create/user', methods=['POST'])
def create_user():
    data = {
        "fname": request.form['fname'],
        "lname" : request.form["lname"],
        "email" : request.form["email"]
    }
    user_id = User.save(data)
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:id_num>')
def view_user(id_num):
    data = {
        'id': id_num
    }
    user = User.get_single_user(data)
    
    return render_template('view.html', user = user)

@app.route('/users/<int:id_num>/edit')
def edit_user(id_num):
    data = {
        'id': id_num
    }
    user= User.get_single_user(data)
    return render_template('edit.html', user = user)

@app.route("/edit/user/<int:id_num>", methods=['POST'])
def submit_edit(id_num):
    data = {
        'id': id_num,
        'fname': request.form['fname'],
        'lname': request.form["lname"],
        'email': request.form["email"]
    }
    User.update_user(data)
    
    return redirect(f'/users/{id_num}')

@app.route("/users/<int:id_num>/delete")
def delete_user(id_num):
    data = {
        'id': id_num
    }
    print(data)
    User.delete_user(data)
    return redirect('/')
