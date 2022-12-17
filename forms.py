from wtforms import Form, StringField, DecimalField, IntegerField, TextAreaField, PasswordField, validators

class RegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    username = StringField('Username', [validators.Length(min=4,max=25)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')