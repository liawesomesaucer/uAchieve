from datetime import datetime

class User(db.Model):

	"""The database for current users"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	email = db.Column(db.String(80), unique=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80), unique=True)

	def __init__(self, name, email, password, username):

		self.name = name
		self.email = email
		self.username = username
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def show_tasks(self):
		return '<Tasks: %r>' % self.tasks.all()

	def __repr__(self):
		return '<User %r>' % self.username


class Task(db.Model):

	"""The database for current tasks"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	description = db.Column(db.String(80))
	deadline = db.Column(db.Integer)
	private = db.Column(db.Boolean)
	start_date = db.Column(db.DateTime)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', 
		backref=db.backref('tasks', lazy='dynamic'))

	def __init__(self, name, description, deadline, private, 
				user, anythin=None,start_date=None):

		# the inputted stuff
		self.name = name
		self.description = description
		self.deadline = deadline
		self.private = private

		# set the start datetime (not entered by user)
		if start_date is None:
			start_date = datetime.utcnow()
		self.start_date = start_date

		# backref user (or something like that)
		self.user = user

	def show_data(self):

		return self.name, self.description, self.deadline, self.start_date, self.user

	def __repr__(self):
		return '<Task %r>' % self.name

class PastTask(Task):

	"""The database for past tasks"""
	