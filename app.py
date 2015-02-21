"""uAchieve is a social network for task accomplishment.  Get 
your favorite and desired tasks done, and keep your friends
updated on what you achieve!  (You'll have the option to keep
your stuff private too!)  Start becoming productive using
uAchieve! """

"""Current objective: 
	1. add a place for past tasks
	2. create task removal
	3. differentiate tasks between users
	4. test to see if other users can see"""


from flask import Flask, render_template, flash, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (LoginManager, login_required, 
					login_user, logout_user, current_user)

app = Flask(__name__)

WTF_CSRF_ENABLED = True
app.secret_key='u_can_do_this'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_repo/info.db'
db = SQLAlchemy(app)
SQLALCHEMY_DATABASE_URI = 'sqlite:///db_repo/info.db'

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

from models import *
from forms import *

@app.route('/index', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def index():
	# render the forms
	register_form = RegisterForm()
	login_form = LoginForm()

	if request.method=='POST':

		# temp debug (ignore)
		print('login then register')
		print(login_form.validate_on_submit())
		print(register_form.validate_on_submit())

		# registration
		if register_form.validate_on_submit():

			print('register_form validated')

			# create a new user object
			user = User(register_form.name.data, 
						register_form.email.data, 
						register_form.username.data, 
						register_form.password.data)

			# add user to db
			db.session.add(user)
			db.session.commit()

			# login this new user
			login_user(user)

			return redirect('/firsttask')

		# logging in form validation
		if login_form.validate_on_submit():

			print('Attempt login')

			#check for user in db
			user = User.query.filter_by(username=login_form.username.data).first()
			
			# if the passwords match
			if (user and login_form.password.data == user.password):
				
				# login the user
				login_user(user)

				print('current user is ')
				print(current_user)
				print(current_user.name)
				return redirect('/home')

			# user is not in our db! turn him baaaack
			elif not user:
				flash('wrong username/password')
				return redirect('/index')
		
		return redirect('/index')

	return render_template('index.html',
							title='Welcome',
							form=register_form,
							login_form=login_form)

@app.route('/home', methods=["GET", "POST"])
@login_required
def home():

	# this guy's name
	name = current_user.name

	# How am I going to get the tasks to display

	# This gets all the tasks in the task db to display
	current_tasks = Task.query.all()
	if current_tasks:
		current_tasks.reverse()

	# Iterate through the tasks
	for task in current_tasks:
		if task.user == current_user:
			print(task)

	return render_template('home.html',
							title='Home',
							name=name,
							tasks=current_tasks)

# for the user's first task
@app.route('/firsttask', methods=["GET", "POST"])
@login_required
def firsttask():

	return render_template('firsttask.html',
							title='Welcome!')


@app.route('/newtask', methods=["GET", "POST"])
@login_required
def newtask():

	form = NewTaskForm()

	if request.method == 'POST':

		task = Task(form.name.data,
					form.description.data,
					form.deadline.data,
					form.private.data,

					# we use the current user
					# I need a better way to reference this
					current_user)

		print('this thing just in')
		print(task)

		# add task and references to db
		db.session.add(task)
		db.session.commit()

		# FOR SOME REASON THE COMMENTED STUFF DOESNT WORK
		# if form.validate_on_submit():
		# 	print('do i get here3')
		# 	print(task)

		# 	return redirect('/home')

		print(current_user.show_tasks())

		return redirect('/home')

	return render_template('newtask.html',
							title='New Task',
							form=form)

@app.route("/tasks/<taskname>")
def tasks(taskname):
	this_task = Task.query.filter_by(name=taskname).first()
	print(this_task)
	if this_task is None:
		print("it errored out")
		flash("error: task not found")
		return redirect('home')
	return render_template('/view_task.html',
							task=this_task,
							title=this_task.name)

@app.route("/users/<username>")
def users(username):
	this_user = User.query.filter_by(name=username).first()
	if this_user is None:
		print("it errored out")
		return redirect('home')
		flash("error: user not found")
	return render_template('/view_user.html',
							user=this_user,
							title=this_user.name,
							user_tasks=this_user.tasks)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

# deals with unauthorized page access
@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    flash("You'll need to log in or sign up to access that page")
    return redirect('/')