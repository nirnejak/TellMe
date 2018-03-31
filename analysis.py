# Librarys
from flask import request
from flask import jsonify
from flask import render_template
from flask import url_for
from flask import redirect

# Importing the Application Modules
from app import app
from libs.eltscript import prepareDB
from libs.decorators import *

# Librarys
import psycopg2 as pg2

# Connecting to database
conn = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")


# Views

# SyncDB - Copy Necessory Files from General Database and Copy them to Analysis Database
@app.route('/syncDB', methods = ['GET','POST'])
@is_logged_in
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
@is_logged_in
def optimizeDB():
	if request.method == 'POST':
		pass
	else:
		res = {
			"status":"success"
		}
	return jsonify(res)

# FetchDB - Returns raw Data in JSON Format based on arguments passed through request.
@app.route('/prepareDB', methods = ['GET','POST'])
@is_logged_in
def fetchDB():
	try:
		prepareDB()
		return jsonify({"status":"success"})
	except:
		return jsonify({"status":"failed"})