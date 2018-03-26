# Librarys
from flask import request
from flask import jsonify
from flask import render_template
from flask import url_for
from flask import redirect

# Importing the Application Modules
from app import app

# Librarys
import psycopg2 as pg2

# Connecting to database
conn = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")


# Views
# SyncDB - Copy Necessory Files from General Database and Copy them to Analysis Database
@app.route('/syncDB', methods = ['GET','POST'])
def syndDB():
	if request.method == 'POST':
		pass
	else:
		res = {
			"status":"success"
		}
	return jsonify(res)

# OptimizeDB - Copy Necessory Files from General Database and Copy them to Analysis Database
@app.route('/optmizeDB', methods = ['GET','POST'])
def optimizeDB():
	if request.method == 'POST':
		pass
	else:
		res = {
			"status":"success"
		}
	return jsonify(res)

# FetchDB - Returns raw Data in JSON Format based on arguments passed through request.
@app.route('/fetchDB', methods = ['GET','POST'])
def fetchDB():
	if request.method == 'POST':
		data = request.get_json()
		res = {
			"status":"success"
		}
	else:
		res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }

	return jsonify(res)