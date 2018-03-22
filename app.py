# -*- coding: utf-8 -*-
# Librarys
from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
# Variables
app = Flask(__name__)

# Settings
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret'


def myfun():
	return "Hi there"

# Views
@app.route('/test', methods=['GET'])
def youtfun():
	return myfun()

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    return render_template('visualize.html')

@app.route('/geomaps', methods=['GET', 'POST'])
def geomaps():
    return render_template('geomaps.html')

@app.route('/export', methods=['GET', 'POST'])
def export():
    return render_template('export.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

@app.route('/tables', methods=['GET', 'POST'])
def tables():
    return render_template('tables.html')

@app.route('/typography', methods=['GET', 'POST'])
def typography():
    return render_template('typography.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')

# Run
if __name__ == '__main__':
    app.run()
