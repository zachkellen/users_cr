from flask import Flask, render_template, request, redirect, url_for
from users import User
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/')
def readAll():
    users = User.get_all()
    print(users)
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
    looking_for = id_num
    query = f"SELECT * FROM users WHERE id = {looking_for};"
    results = connectToMySQL('users_schema').query_db(query)
    user_id = id_num
    full_name = f"{results[0]['first_name']} {results[0]['last_name']}"
    email = results[0]['email']
    created_on = results[0]['created_at']
    last_updated = results[0]['updated_at']
    return render_template('view.html', user_id = user_id, full_name = full_name, email = email, created_on = created_on, last_updated = last_updated)

@app.route('/users/<int:id_num>/edit')
def edit_user(id_num):
    looking_for = id_num
    query = f"SELECT * FROM users WHERE id = {looking_for};"
    results = connectToMySQL('users_schema').query_db(query)
    first_name = results[0]['first_name']
    last_name = results[0]['last_name']
    email = results[0]['email']
    return render_template('edit.html', user_id = id_num, first_name = first_name, last_name = last_name, email = email)

@app.route("/edit/user/<int:id_num>", methods=['POST'])
def submit_edit(id_num):
    fname = request.form['fname']
    lname = request.form["lname"]
    email = request.form["email"]
    query = f"UPDATE users SET first_name='{fname}',last_name='{lname}',email='{email}' WHERE id={id_num};"
    connectToMySQL('users_schema').query_db(query)
    return redirect(f'/users/{id_num}')

@app.route("/users/<int:id_num>/delete")
def delete_user(id_num):
    query = f"DELETE FROM users WHERE id = {id_num};"
    connectToMySQL('users_schema').query_db(query)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)