# Librarys
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import jsonify

import psycopg2 as pg2

# Importing the Application Modules
from app import app
from libs.data import stateData

# Views

# Index
@app.route('/', methods=['GET'])
def index():
	if request.method == 'POST':
		pass
	return redirect(url_for('dashboard'))

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	if request.method == 'POST':
		pass
	return render_template('dashboard.html')

# Visualize Section
@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
	if request.method == 'POST':
		pass
	return render_template('visualize.html')

# Geomaps Section
@app.route('/geomaps', methods=['GET', 'POST'])
def geomaps():
	if request.method == 'POST':
		pass
	return render_template('geomaps.html')

# Export Data Section
@app.route('/export', methods=['GET', 'POST']) 
def export():
	if request.method == 'POST':
		data = request.get_json()

		dateFrom = data["dateFrom"]
		dateTo = data["dateTo"]
		state = data["state"]
		district = data["district"]
	else:
		try:
			# Connecting to database
			conn = pg2.connect(database="db70oouohkh4bj",user="fnqryfoivwpuxd",password="884e1a40af2227d023c58401914873dfea4d44530a34647bb5930872b1a21807",host="ec2-54-221-220-59.compute-1.amazonaws.com",port="5432")

			# Creating cursor
			cur = conn.cursor()

            # Executing Query
			cur.execute("SELECT DISTINCT district FROM location_dim ORDER BY district;")

			# Fetching Data
			districtData = cur.fetchall()

			# Executing Query
			cur.execute("SELECT DISTINCT crop_name FROM crop_dim ORDER BY crop;")

			# Fetching Data
			cropData = cur.fetchall()

			# Executing Query
			cur.execute("SELECT DISTINCT water_source FROM fact_table ORDER BY source;")

			# Fetching Data
			sourceData = cur.fetchall()
		except:
			conn.rollback()
			res = {
                "status" : "failed",
                "message" : "Something went wrong",
                "error" : ""
            }
			return jsonify(res)

        # Commiting the Changes
		conn.commit()

        # Closing the cursor
		cur.close()

		# Closing the connection
		conn.close()
		
		data = {
			"stateData" : stateData,
			"districtData" : districtData,
			"cropData" : cropData,
			"sourceData" : sourceData
		}
	return render_template('export.html', data = data)

# User Management Section
@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

# Broadcast Message Section
@app.route('/message', methods=['GET', 'POST'])
def message():
	if request.method == 'POST':
		pass
	data = {
			"stateData" : stateData,
			"district" : "district"
		}
	return render_template('message.html', data = data)

# User Settings Section
@app.route('/settings', methods=['GET', 'POST'])
def settings():
	if request.method == 'POST':
		pass
	return render_template('settings.html')