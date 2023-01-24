from wtforms import Form, StringField, DecimalField, IntegerField, TextAreaField, PasswordField, validators, SelectField
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
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class PatientRegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class ResearcherRegisterForm(Form):
    institute_id = IntegerField('Institute ID', [validators.DataRequired()])
    institute_name = StringField('Institute Name', [validators.DataRequired()])
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')