from wtforms import StringField, Form, StringField, BooleanField, PasswordField, validators

class RegistrationForm(Form):
    name = StringField("Name", [validators.Length(min=3, max=40)])
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=64), validators.Email()])
    password = PasswordField("New Password", [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords must match")
    ])
    confirm = PasswordField("Repeat Password")

class LoginForm(Form):
    email = StringField("Email", [validators.Length(min=6, max=64), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])