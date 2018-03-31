from flask import url_for
from flask import flash
from flask import session
from flask import redirect
from functools import wraps


# Check if user is not logged in
def is_not_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if not('logged_in' in session):
			return f(*args, **kwargs)
		else:
			flash('You are already Logged In','warning')
			return redirect(url_for('dashboard'))
	return wrap

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('index'))
	return wrap

# Check if user is superuser
def as_superuser(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['userType'] in ["SUPER"]:
			return f(*args, **kwargs)
		else:
			session.clear()
			flash('Not Enough Privilages!','danger')
			return redirect(url_for('index'))
	return wrap


# Check if user is admin
def as_admin(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['userType'] in ["ADMIN","SUPER"]:
			return f(*args, **kwargs)
		else:
			session.clear()
			flash('Not Enough Privilages!','danger')
			return redirect(url_for('index'))
	return wrap

# Check if user is analyst
def as_analyst(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['userType'] in ["ANALYST","ADMIN","SUPER"]:
			return f(*args, **kwargs)
		else:
			session.clear()
			flash('Not Enough Privilages!','danger')
			return redirect(url_for('index'))
	return wrap

# Check if user is farmer
def as_farmer(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['userType'] == "FARMER":
			return f(*args, **kwargs)
		else:
			session.clear()
			flash('These features are meant to be acessed by Farmer!','danger')
			return redirect(url_for('index'))
	return wrap
