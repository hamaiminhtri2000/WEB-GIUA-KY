from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, email_validator

class SignUpForm(FlaskForm):
    inputFirstName = StringField('First name',[DataRequired(message="Please enter your first name")])
    inputLastName = StringField('Last name',[DataRequired(message="Please enter your last name")])
    inputEmail = StringField('Email address', [Email(message='Not a valid email address'),
        DataRequired(message="Please enter your email address")])
    inputPassword = PasswordField('Password',[InputRequired(message="Please enter your password!"), EqualTo('inputConfirmPassword', message="Passwords does not match!!")])
    inputConfirmPassword = PasswordField('Confirm password')
    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    inputEmail = StringField('Email address',
        [Email(message='Not a valid email address'),
        DataRequired(message="Please enter your email address")])
    inputPassword = PasswordField('Password',
        [InputRequired(message="Please enter your password!")])
    submit = SubmitField('Sign In')

class AddTaskForm(FlaskForm):
    inputTask = StringField('Task',
        [DataRequired(message="Please enter your task")])
    inputPriority = SelectField('Priority', coerce = int)
    submit = SubmitField('Add')

class AddProjectForm(FlaskForm):
    inputProjectName = StringField('Project name',
        [DataRequired(message="Please enter your project name")])
    inputDescription = StringField('Description',
        [DataRequired(message="Please enter your project description")])
    inputDealine = DateTimeLocalField('Project deadline',
    validators=[DataRequired()],format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Add')

    