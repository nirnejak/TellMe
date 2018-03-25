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
@app.route('/fetchDB', method = ['GET','POST'])
def fetchDB():
	return "Hi there"