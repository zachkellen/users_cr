from flask import Flask, render_template, request, redirect
from users import User

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
    User.save(data)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)