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
from libs.eltscript import prepareDB

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
	conn = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")

	try:
		# Creating cursor
		cur = conn.cursor()

        # Executing Query
		cur.execute("SELECT users_active from dashboard;")

		# Fetching Data
		usersActive = cur.fetchall()

		# Executing Query
		cur.execute("SELECT total_farms from dashboard;")

		# Fetching Data
		totalFarms = cur.fetchall()

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
		"usersActive" : usersActive,
		"totalFarms" : totalFarms
	}
	# return jsonify(data)

	return render_template('dashboard.html', data = data)

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
		# Connecting to database
		conn = pg2.connect(database="db70oouohkh4bj",user="fnqryfoivwpuxd",password="884e1a40af2227d023c58401914873dfea4d44530a34647bb5930872b1a21807",host="ec2-54-221-220-59.compute-1.amazonaws.com",port="5432")

		try:
			# Creating cursor
			cur = conn.cursor()

            # Executing Query
			cur.execute("SELECT DISTINCT district FROM location_dim ORDER BY district;")

			# Fetching Data
			districtData = cur.fetchall()

			# Executing Query
			cur.execute("SELECT DISTINCT crop_name FROM crop_dim ORDER BY crop_name;")

			# Fetching Data
			cropData = cur.fetchall()

			# Executing Query
			cur.execute("SELECT DISTINCT water_source FROM fact_table ORDER BY water_source;")

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
		state = form.data["state"]
		district = form.data["district"]
		crop = form.data["crop"]
		irrigationSource = form.data["irrigationSource"]
		messageBody = form.data["messageBody"]
		messageLink = form.data["messageLink"]
		messageType = form.data["messageType"]
	else:
		# Connecting to database
		conn = pg2.connect(database="db70oouohkh4bj",user="fnqryfoivwpuxd",password="884e1a40af2227d023c58401914873dfea4d44530a34647bb5930872b1a21807",host="ec2-54-221-220-59.compute-1.amazonaws.com",port="5432")

		try:
			# Creating cursor
			cur = conn.cursor()

            # Executing Query
			cur.execute("SELECT DISTINCT district FROM location_dim ORDER BY district;")

			# Fetching Data
			districtData = cur.fetchall()

			# Executing Query
			cur.execute("SELECT DISTINCT crop_name FROM crop_dim ORDER BY crop_name;")

			# Fetching Data
			cropData = cur.fetchall()

			# Executing Query
			cur.execute("SELECT DISTINCT water_source FROM fact_table ORDER BY water_source;")

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
	return render_template('message.html', data = data)

# User Settings Section
@app.route('/settings', methods=['GET', 'POST'])
def settings():
	if request.method == 'POST':
		pass
	return render_template('settings.html')