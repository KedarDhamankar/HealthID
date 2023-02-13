from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_file
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps
from sqlhelpers import *
from forms import *

from filestack import Client

from io import BytesIO

from datetime import datetime,date
import time

client = Client("A0qg3V3jRiyTufmfEmUcgz")
allowed_extensions = ['pdf']

#initialize the app
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize mysql
mysql = MySQL(app)

# check if file extension matches
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


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
    session['institute_id'] = user.get('institute_id')
    session['institute_name'] = user.get('institute_name')
    session['organisation_id'] = user.get('organisation_id')
    session['organisation_name'] = user.get('organisation_name')
    session['licensenum'] = user.get('licensenum')
    session['email'] = user.get('email')

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
            # sql = "insert into users values('Doctor',%s,%s,%s,%s,%s,%s)"
            # val = (name,email,None,None,license_num,password)
            sql = "insert into users values('Doctor',%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (name,email,None,None,license_num,None,None,password)
            cur.execute(sql,val)
            mysql.connection.commit()
            cur.close()
            log_in_user(email)
            return redirect(url_for('docdashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('docregister'))

    return render_template('docregister.html', form=form)

#Researcher's Registration Page
@app.route("/resregister", methods = ['GET', 'POST'])
def resregister():
    form = ResearcherRegisterForm(request.form)
    users = Table("users", "category", "name", "email","institute_id", "institute_name","organisation_id", "organisation_name", "license_num", "password")

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
            # sql = "insert into users values('Researcher',%s,%s,%s,%s,%s,%s)"
            # val = (name,email,institute_id,institute_name,None,password)
            sql = "insert into users values('Researcher',%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (name,email,institute_id,institute_name,None,None,None,password)
            cur.execute(sql,val)
            mysql.connection.commit()
            cur.close()
            log_in_user(email)
            return redirect(url_for('resdashboard'))
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
            # sql = "insert into users values('Patient',%s,%s,%s,%s,%s,%s)"
            # val = (name,email,None,None,None,password)
            sql = "insert into users values('Patient',%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (name,email,None,None,None,None,None,password)
            cur.execute(sql,val)
            mysql.connection.commit()
            cur.close()
            log_in_user(email)
            return redirect(url_for('patdashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('patregister'))

    return render_template('patregister.html', form=form)

#Organisation's Registration Page
@app.route("/orgregister", methods = ['GET', 'POST'])
def orgregister():
    form = OrganisationRegisterForm(request.form)
    # users = Table("users", "category", "name", "email","institute_id", "institute_name", "license_num", "password")

    #if form is submitted
    if request.method == 'POST' and form.validate():
        #collect form data
        organisation_name = form.organisation_name.data
        organisation_id = form.organisation_id.data
        email = form.email.data
        print(organisation_id)
        print(organisation_name)
        print(email)
        #make sure user does not already exist
        if isnewuser(email):
            #add the user to mysql and log them in
            password = sha256_crypt.encrypt(form.password.data)
            print('password - ', form.password.data)
            if len(form.password.data)>=4:
                cur = mysql.connection.cursor()
                sql = "insert into users values('Organisation',%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (None,email,None,None,None,organisation_name,organisation_id,password)
                cur.execute(sql,val)
                mysql.connection.commit()
                cur.close()
                log_in_user(email)
                print('worked')
                return redirect(url_for('orgdashboard'))
            else:
                # print('small)
                # flash("Email is not found", 'danger')
                flash("Password must have at least 4 letters!", 'danger')
                return(redirect(url_for('orgregister')))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('orgregister'))

    return render_template('orgregister.html', form=form)

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
                message_popup = 1
                flash('You are now logged in.', 'success')
                if category == 'Doctor':
                    return redirect(url_for('docdashboard'))
                elif category == 'Patient':
                    return redirect(url_for('patdashboard'))
                elif category == 'Researcher':
                    return redirect(url_for('resdashboard'))
                elif category == 'Organisation':
                    return redirect(url_for('orgdashboard'))
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

#Doctor Dashboard
@app.route("/docdashboard", methods = ['GET', 'POST'])
@is_logged_in
def docdashboard():
    visitform = PatientVisit(request.form)
    cur = mysql.connection.cursor()
    doctor_name = session.get('name')

    #Displaying appointments on the Doctor Dashboard
    result = cur.execute("select * from appointments where doctor_name = \"%s\"" %(doctor_name))
    i=0
    appointments = []
    if result>0:
        message_popup=1
        while i<result:
            appointments.append(cur.fetchone())
            i+=1
        cur.close()
    else:
        message_popup = 0
        flash('No Upcoming Appointments','warning')
    #submit the patient prescription to backend
    if request.method == 'POST' and form.validate(): 
        appoint_desc = visitform.description.data
        remarks = visitform.remarks.data
        prescription = visitform.prescription.data
        presc_table = Table("prescription","patient_name","patient_email","hospital_name","appoint_desc","remarks","prescription")
        # cur = mysql.connection.cursor()
        # sql = "insert into prescription values(,%s,%s,%s,%s,%s,%s,%s,%s)"
        # val = (patient_name,patient_email,hospital_name,appoint_desc,remarks,prescription)
        # cur.execute(sql,val)
        # mysql.connection.commit()
        # cur.close()

    return render_template('docdashboard.html', session=session, appointments=appointments, message_popup=message_popup)

#Patient Dashboard
@app.route("/patdashboard", methods = ['GET', 'POST'])
@is_logged_in
def patdashboard():

    #Booking an appointment
    appform = BookAppointmentForm(request.form)
    patient_email = session['email']
    patient_name = session['name']
    if request.method == 'POST' and appform.validate():
        hospital_name = appform.hospital_name.data
        doctor_name = appform.doctor_name.data
        date = appform.date.data
        time = appform.time.data
        print("hospital = ",hospital_name)
        print("doctor - ", doctor_name)
        print("date - ", date)
        cur = mysql.connection.cursor()
        sql = "insert into appointments values(%s,%s,%s,%s,%s,%s)"
        val = (doctor_name, patient_email, patient_name, hospital_name, date, time)
        cur.execute(sql,val)
        mysql.connection.commit()
        cur.close()
        flash('Appointment Booked', 'success ')

    #To display upcoming appointment
    cur=mysql.connection.cursor()
    app_count=cur.execute("select * from appointments where patient_email=\"%s\" and visited='no' " %(patient_email))
    if app_count>0:
        appointment = cur.fetchone()
    cur.close()

    #To display all prescriptions
    cur=mysql.connection.cursor()
    presc_count=cur.execute("select * from prescription where patient_email=\"%s\"" %(patient_email))
    prescriptions=[]
    if presc_count>0:
        prescriptions.append(cur.fetchone())
    cur.close()

    #To display all reports
    cur=mysql.connection.cursor()
    reports_count=cur.execute("select * from prescription where patient_email=\"%s\"" %(patient_email))
    reports=[]
    if reports_count>0:
        reports.append(cur.fetchone())
    cur.close()

    return render_template('patdashboard.html', form=appform, session=session, appointment=appointment, prescriptions=prescriptions, reports=reports)

#Researcher Dashboard
@app.route("/resdashboard", methods = ['GET', 'POST'])
@is_logged_in
def resdashboard():
    # Upload Paper Form
    upload_form = PaperUpload(request.form)
    author = session['name']
    email = session['email']
    institute_id = session['institute_id']
    institute_name = session['institute_name']
    today = date.today()
    time = datetime.now()
    current_date = today.strftime("%B %d, %Y")
    current_time = time.strftime("%H:%M:%S")
    # flash('Logged In!', 'success')
    if request.method == 'POST' and upload_form.validate():
        paper_name = upload_form.paper_name.data
        paper_category = upload_form.paper_category.data
        # paper_id = 2
        file = request.files['myfile']
        file.save(file.filename)
        filepath=file.filename
        # file_contents = file.read()
        print("file - ",file)
        # file_stream = BytesIO(file.read())
        filelink = client.upload(filepath=filepath)
        paper_url = filelink.url
        cur = mysql.connection.cursor()
        sql = "insert into papers values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (author, email, institute_id, institute_name, None, None, paper_name, paper_url, paper_category, current_date, current_time)
        cur.execute(sql,val)
        mysql.connection.commit()
        cur.close()
        upload_paper(paper_url)
        print("PaperName = ",paper_name)
        flash('Paper Uploaded!', 'success')
        return(redirect(url_for('resdashboard')))

    #Displaying research papers on Researcher Dashboard
    cur = mysql.connection.cursor()
    pdf_count = cur.execute("select * from papers")
    print("count = ", pdf_count)
    i=0
    pdf_list = []
    while i<pdf_count:
        pdf_list.append(cur.fetchone())
        i+=1
    cur.close()
    # print(pdf_list)

    # Search Option
    search_form = SearchPaper(request.form)
    if request.method=='POST' and search_form.validate():
        keyword = search_form.search.data
        cur = mysql.connection.cursor()
        count = cur.execute("select * from papers where category = \"%s\"" %(keyword))
        i=0
        global search_results
        search_results = []
        while i<count:
            search_results.append(cur.fetchone())
            i+=1
        cur.close()
        print("result - ", search_results)
    return render_template('resdashboard.html', form=form, session=session, pdf_list=pdf_list)

#Organisation Dashboard
@app.route("/orgdashboard", methods = ['GET', 'POST'])
def orgdashboard():
    org_name = session['organisation_name']

    #Displaying patient records on the dashboard
    cur = mysql.connection.cursor()
    result = cur.execute("select * from prescription where hospital_name = \"%s\"" %(org_name))
    i=0
    records = []
    print(result)
    while i<result:
        records.append(cur.fetchone())
        i+=1
    cur.close()
    
    #Displaying patient reports on the dashboard
    cur = mysql.connection.cursor()
    result = cur.execute("select * from reports where hospital_name = \"%s\"" %(org_name))
    i=0
    reports = []
    print(result)
    while i<result:
        reports.append(cur.fetchone())
        i+=1
    cur.close()

    #Upload Reports
    report_form = ReportUpload(request.form)
    hospital_name = session['organisation_name']
    today = date.today()
    current_date = today.strftime("%B %d, %Y")
    if request.method == 'POST' and report_form.validate():
        patient_email = report_form.patient_email.data
        report_name = report_form.report_name.data
        users = Table("users", "category", "name", "email", "password")
        user = users.getone("email", patient_email)
        print('user -', user)
        patient_name = user.get('name')
        file = request.files['myfile']
        file.save(file.filename)
        filepath=file.filename
        filelink = client.upload(filepath=filepath)
        report_url = filelink.url
        cur = mysql.connection.cursor()
        sql = "insert into reports values(%s,%s,%s,%s,%s,%s)"
        val = (patient_name, patient_email, hospital_name, report_name, report_url, current_date)
        cur.execute(sql,val)
        mysql.connection.commit()
        cur.close()
        # upload_paper(paper_url)
        # print("PaperName = ",paper_name)
        flash("Report Uploaded!", "success")
        return(redirect(url_for('orgdashboard')))
    return render_template('orgdashboard.html', session=session, records=records, reports=reports)

#Services page
@app.route("/services")
def services():
    return render_template('services.html')

#Index page
@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')

#404 Error Handler
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


#Run app
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)