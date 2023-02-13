from wtforms import Form, StringField, TimeField, DateField, IntegerField, TextAreaField, PasswordField, validators, SelectField
from flask_wtf import *

class RegisterForm(Form):
    choices=[('Admin','Admin'),('Doctor','Doctor'),('Patient','Patient'),('Researcher','Researcher')]
    category = SelectField('Select a Category', choices=choices)
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class DoctorRegisterForm(Form):
    license_num = StringField('License Number', [validators.Length(min=1,max=50)] )
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4,max=50), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class PatientRegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4,max=50), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class ResearcherRegisterForm(Form):
    institute_id = IntegerField('Institute ID', [validators.DataRequired()])
    institute_name = StringField('Institute Name', [validators.DataRequired()])
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4,max=50), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class OrganisationRegisterForm(Form):
    organisation_name = StringField('Institute Name', [validators.DataRequired()])
    organisation_id = IntegerField('Institute ID', [validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4,max=50), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class BookAppointmentForm(Form):
    hospital_name = StringField("Hospital Name", [validators.DataRequired()])
    doctor_name = StringField("Doctor Name", [validators.DataRequired()])
    date = DateField("Date", [validators.DataRequired()])
    time = TimeField("Time", [validators.DataRequired()])

class PatientVisit(Form):
    description = StringField("Appointment Description ", [validators.DataRequired()])
    remarks = StringField("Ailment", [validators.DataRequired()])    
    prescription = StringField("Prescription", [validators.DataRequired()])

class PaperUpload(Form):
    paper_name = StringField("Paper Name", [validators.DataRequired()])
    paper_category = StringField("Paper Category", [validators.DataRequired()])

class ReportUpload(Form):
    patient_email = StringField("Patient Email", [validators.DataRequired()])
    report_name = StringField("Report Name", [validators.DataRequired()])

class SearchPaper(Form):
    search = StringField("Search Keyword", [validators.DataRequired()])