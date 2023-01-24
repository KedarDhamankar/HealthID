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
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize mysql
mysql = MySQL(app)

#wrap to define if the user is currently logged in from session
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login.", "danger")
            return redirect(url_for('login'))
    return wrap

#log in the user by updating session
def log_in_user(email):
    users = Table("users", "category", "name", "email","institute_id", "institute_name", "license_num", "password")
    user = users.getone("email", email)

    session['logged_in'] = True
    session['name'] = user.get('name')
    session['email'] = user.get('email')

#Registration page
# @app.route("/register", methods = ['GET', 'POST'])
# def register():
#     form = RegisterForm(request.form)
#     # users = Table("users","category", "name", "email", "password")
#     # users = Table("user", "name", "email", "password")

#     #if form is submitted
#     if request.method == 'POST' and form.validate():
#         #collect form data
#         category = form.category.data
#         email = form.email.data
#         name = form.name.data
#         print('category',category)
#         print('email',email)
#         print('name',name)
#         password = sha256_crypt.encrypt(form.password.data)
#         cur = mysql.connection.cursor()
#         cur.execute("insert into users values('%s','%s','%s','%s')" %(category,name,email,password))
#         # cur.execute("insert into user values('%s','%s','%s')" %(name,email,password))
#         mysql.connection.commit()
#         cur.close()
#         #make sure user does not already exist
#         # if isnewuser(name):
#         #     #add the user to mysql and log them in
#         #     password = sha256_crypt.encrypt(form.password.data)
#         #     cur = mysql.connection.cursor()
#         #     # cur.execute("insert into users values('%s','%s','%s','%s')" %(category,name,email,password))
#         #     cur.execute("insert into user values('%s','%s','%s')" %(name,email,password))
#         #     mysql.connection.commit()
#         #     cur.close()
#         #     log_in_user(name)
#         #     return redirect(url_for('dashboard'))
#         # else:
#         #     flash('User already exists', 'danger')
#         #     return redirect(url_for('register'))

#     return render_template('register.html', form=form)

#Doctor's Registration Page
@app.route("/docregister", methods = ['GET', 'POST'])
def docregister():
    form = DoctorRegisterForm(request.form)
    users = Table("users", "category", "name", "email","institute_id", "institute_name", "license_num", "password")

    #if form is submitted
    if request.method == 'POST' and form.validate():
        #collect form data
        license_num = form.license_num.data
        email = form.email.data
        name = form.name.data

        #make sure user does not already exist
        if isnewuser(email):
            #add the user to mysql and log them in
            password = sha256_crypt.encrypt(form.password.data)
            cur = mysql.connection.cursor()
            sql = "insert into users values('Doctor',%s,%s,%s,%s,%s,%s)"
            val = (name,email,None,None,license_num,password)
            cur.execute(sql,val)
            mysql.connection.commit()
            cur.close()
            log_in_user(email)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('docregister'))

    return render_template('docregister.html', form=form)

#Researcher's Registration Page
@app.route("/resregister", methods = ['GET', 'POST'])
def resregister():
    form = ResearcherRegisterForm(request.form)
    users = Table("users", "category", "name", "email","institute_id", "institute_name", "license_num", "password")

    #if form is submitted
    if request.method == 'POST' and form.validate():
        #collect form data
        institute_name = form.institute_name.data
        institute_id = form.institute_id.data
        email = form.email.data
        name = form.name.data

        #make sure user does not already exist
        if isnewuser(email):
            #add the user to mysql and log them in
            password = sha256_crypt.encrypt(form.password.data)
            cur = mysql.connection.cursor()
            sql = "insert into users values('Researcher',%s,%s,%s,%s,%s,%s)"
            val = (name,email,institute_id,institute_name,None,password)
            cur.execute(sql,val)
            mysql.connection.commit()
            cur.close()
            log_in_user(email)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('resregister'))

    return render_template('resregister.html', form=form)

#Researcher's Registration Page
@app.route("/patregister", methods = ['GET', 'POST'])
def patregister():
    form = PatientRegisterForm(request.form)
    users = Table("users", "category", "name", "email","institute_id", "institute_name", "license_num", "password")

    #if form is submitted
    if request.method == 'POST' and form.validate():
        #collect form data
        email = form.email.data
        name = form.name.data

        #make sure user does not already exist
        if isnewuser(email):
            #add the user to mysql and log them in
            password = sha256_crypt.encrypt(form.password.data)
            cur = mysql.connection.cursor()
            sql = "insert into users values('Patient',%s,%s,%s,%s,%s,%s)"
            val = (name,email,None,None,None,password)
            cur.execute(sql,val)
            mysql.connection.commit()
            cur.close()
            log_in_user(email)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('patregister'))

    return render_template('patregister.html', form=form)

#Login page
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #if form is submitted
    if request.method == 'POST':
        #collect form data
        category = request.form['category']
        email = request.form['email']
        candidate = request.form['password']
        print('category - ', category)
        print('email - ', email)
        print('password - ', candidate)
        #access users table to get the user's actual password
        users = Table("users", "category", "name", "email", "password")
        user = users.getone("email", email)
        print('user -', user)
        accPass = user.get('password')
        name = user.get('name')
        cat = user.get('category')
        #if the password cannot be found, the user does not exist
        if accPass is None:
            flash("Email is not found", 'danger')
            return redirect(url_for('login'))
        else:
            #verify that the password entered matches the actual password
            if sha256_crypt.verify(candidate, accPass) and category==cat:
                #log in the user and redirect to Dashboard page
                log_in_user(email)
                flash('You are now logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                #if the passwords do not match
                flash("Invalid credentials", 'danger')
                return redirect(url_for('login'))

    return render_template('login.html')

#logout the user. Ends current session
@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logout success", "success")
    return redirect(url_for('login'))

#Dashboard page
@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template('dashboard.html', session=session)

#Services page
@app.route("/services")
def services():
    return render_template('services.html')

#Index page
@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')


#Run app
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)