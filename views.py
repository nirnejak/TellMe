# Librarys
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import jsonify

import psycopg2 as pg2
import psycopg2.extras as pgext

# Importing the Application Modules
from app import app
from libs.data import stateData
from libs.eltscript import prepareDB
from libs.chloropleth import chloropleth
from libs.export import export_data
from libs.decorators import *

# Views

# Index
@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		# Get Form Fields
		aadharID = request.form['aadharID']
		password_candidate = request.form['password']

		# Connecting to database
		conn = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")

		# Creating cursor
		cur = conn.cursor()

		# Creating cursor
		cur = conn.cursor(cursor_factory=pgext.DictCursor)
        
        # Executing Query
		try:
			cur.execute("SELECT password, name, user_type FROM users WHERE aadhar_id = %s;",[aadharID])
		except:
			conn.rollback()
			res = {
				"status":"failed",
				"message" : "Something went wrong"
			}
			return jsonify(res)

		# Generate Response
		dataRecieved = cur.fetchone()

		# Commiting the Changes
		conn.commit()

		# Closing the cursor
		cur.close()

		if dataRecieved:
			# Compare Passwords
			if password_candidate == dataRecieved['password']:
				session['logged_in'] = True
				session['aadharID'] = aadharID
				session['userType'] = dataRecieved['user_type']

				return redirect(url_for('dashboard'))
			else:
				res = {
                    "type" : "danger",
                    "message" : "Invalid Login"
                }
				return render_template('index.html', res = res)
		else:
			res = {
				"type" : "danger",
				"message" : "Aadhar not Registered"
			}
			return render_template('index.html', res = res)
	return render_template('index.html')

# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	res = {
		"type" : "success",
		"message" : "Invalid Login"
	}
	return redirect(url_for('index'))


# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
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
@is_logged_in
def visualize():
	if request.method == 'POST':
		pass
	return render_template('visualize.html')

# Geomaps Section
@app.route('/geomaps', methods=['GET', 'POST'])
@is_logged_in
def geomaps():
	if request.method == 'POST':
		pass
	else:
		data = chloropleth()
	return render_template('geomaps.html', data = data)

# Export Data Section
@app.route('/export', methods=['GET', 'POST'])
@is_logged_in
def export():
	if request.method == "POST":
		'''
		dateFrom = request.form["dateFrom"]
		dateTo = request.form["dateTo"]
		state = request.form["state"]
		district = request.form["district"]
		crop = request.form["crop"]
		sourceIrrigation = request.form["sourceIrrigation"]

		data = export_data(dateFrom,dateTo,state,district,crop,sourceIrrigation)
		'''
		data = {
			"No data":"nodata"
		}
		return jsonify(data)

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
@is_logged_in
def user():
	if request.method == 'POST':
		aadharID = request.form["aadharID"]
		password = request.form["password"]
		userType = request.form["userType"]


		# Creating Connection
		conn = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")

		try:
			# Creating cursor
			cur = conn.cursor()

			# Executing Query
			cur.execute("INSERT INTO users(aadhar_id, password, name, contact_no, user_type) VALUES(%s,%s,%s,%s,%s)",(aadharID, password, aadharData[aadharID]['name'], aadharData[aadharID]['contact_no'],userType))

			# Commiting into Database
			cur.commit()
			conn.commit()

			# Closing Cursor and Database
			cur.close()
			conn.close()
		except:
			pass
	return render_template('user.html')

# Broadcast Message Section
@app.route('/message', methods=['GET', 'POST'])
@is_logged_in
def message():
	if request.method == 'POST':
		state = request.form["state"]
		district = request.form["district"]
		city = request.form["city"]
		messageBody = request.form["messageBody"]

		# Creating Connection
		conn = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")

		try:
			# Creating cursor
			cur = conn.cursor()

			# Executing Query
			cur.execute("UPDATE users SET message_broadcast = %s WHERE state = %s AND district = %s AND city = %s",(messageBody, state, district, city))

			# Commiting into Database
			cur.commit()
			conn.commit()

			# Closing Cursor and Database
			cur.close()
			conn.close()
		except:
			pass
	
		return render_template('message.html')



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
@is_logged_in
def settings():
	if request.method == 'POST':
		pass
	return render_template('settings.html')