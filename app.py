from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps

from sqlhelpers import *
from forms import *

import time

#initialize the app
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize mysql
mysql = MySQL(app)

#log in the user by updating session
def log_in_user(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

#Registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password")

    #if form is submitted
    if request.method == 'POST' and form.validate():
        #collect form data
        username = form.username.data
        email = form.email.data
        name = form.name.data

        #make sure user does not already exist
        if isnewuser(username):
            #add the user to mysql and log them in
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            log_in_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

#Login page
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #if form is submitted
    if request.method == 'POST':
        #collect form data
        username = request.form['username']
        candidate = request.form['password']

        #access users table to get the user's actual password
        users = Table("users", "name", "email", "username", "password")
        user = users.getone("username", username)
        accPass = user.get('password')

        #if the password cannot be found, the user does not exist
        if accPass is None:
            flash("Username is not found", 'danger')
            return redirect(url_for('login'))
        else:
            #verify that the password entered matches the actual password
            if sha256_crypt.verify(candidate, accPass):
                #log in the user and redirect to Dashboard page
                log_in_user(username)
                flash('You are now logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                #if the passwords do not match
                flash("Invalid password", 'danger')
                return redirect(url_for('login'))

    return render_template('login.html')

#logout the user. Ends current session
@app.route("/logout")
def logout():
    session.clear()
    flash("Logout success", "success")
    return redirect(url_for('login'))

#Dashboard page
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

#Services page
@app.route("/services")
def services():
    return render_template('services.html')

#Index page
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template('index.html')


#Run app
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)