from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired

class RegisterForm(Form):

	name = StringField('name', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	username = StringField('username', validators=[validators.Length(min=6, max=25)])
	password = PasswordField('password', validators=[validators.Length(min=6, max=35)])

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class NewTaskForm(Form):

	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', validators=[DataRequired])
	deadline = StringField('deadline', validators=[DataRequired()])
	private = BooleanField('private')