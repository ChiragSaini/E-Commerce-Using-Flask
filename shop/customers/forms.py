from wtforms import StringField, TextAreaField, PasswordField, SubmitField, IntegerField, validators, Form, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import RegisterModel

class CustomerRegistrationForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    username = StringField('Username', [validators.DataRequired()])
    email = StringField("Email", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message="Both passwords should match")])
    confirm = PasswordField("Repeat Password", [validators.DataRequired()])    
    country = StringField('Country', [validators.DataRequired()])
    state = StringField('State', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    contact = StringField('Contact', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])

    profile_image = FileField("Profile Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], "Images only")])
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        if RegisterModel.query.filter_by(username=username.data).first():
            raise ValidationError("Username already Exists.")

    def validate_email(self, email):
        if RegisterModel.query.filter_by(email=email.data).first():
            raise ValidationError("Email already Exists.")

class CustomerLoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])