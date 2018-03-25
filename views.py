# Librarys
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect

# Importing the Application Modules
from app import app
from data import stateData

# Views

# Index
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('dashboard'))

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

# Visualize Section
@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    return render_template('visualize.html')

# Geomaps Section
@app.route('/geomaps', methods=['GET', 'POST'])
def geomaps():
    return render_template('geomaps.html')

# Export Data Section
@app.route('/export', methods=['GET', 'POST'])
def export():
    return render_template('export.html', stateData = stateData)

# User Management Section
@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

# Broadcast Message Section
@app.route('/message', methods=['GET', 'POST'])
def message():
    return render_template('message.html')

# User Settings Section
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')