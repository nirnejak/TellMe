# -*- coding: utf-8 -*-
# Librarys
from flask import Flask
from flask import request
from flask import jsonify

import psycopg2 as pg2

from passlib.hash import sha256_crypt

# Variables
api = Flask(__name__)

# Settings
api.config['DEBUG'] = True
api.config['SECRET_KEY'] = 'apisecret'


# Views

# GetOTP - Return Success Message if aadhar ID is valid and unregistered
@api.route('/getOTP', methods=['GET', 'POST'])
def getOTP():
    # Receiving Aadhar ID
    aadharID = request.get_json()['aadharID']
    
    if len(aadharID)==12:
    	# Connecting to database
    	conn = pg.connect(database="",user="",password="",host="",port="5432")
    	# Creating cursor
    	cur = conn.cursor()
    	# Executing Query
    	cur.execute("SELECT * FROM users WHERE aadharID = %s",[aadharID])

    	res = {
    		"status" : "success",
    	}
    	return jsonify(res)
    else:
    	res = {
    		"status" : "failed",
    		"message" : "Incorrect Aadhar ID"
    	}
    	return jsonify(res)

# verifyOTP - Return Success Message if OTP sent by the user is correct
@api.route('/verifyOTP', methods=['GET', 'POST'])
def verifyOTP():
    data = request.get_json()
    
    aadharID = data["aadharID"]
    OTP = data["OTP"]

    if 5>2:
    	res = {
    		"status" : "success",
    	}
    	return jsonify(res)
    else:
    	res = {
    		"status" : "failed",
    		"message" : "Incorrect Aadhar OTP"
    	}
    	return jsonify(res)

# Register - Register the User and send Success Message
@api.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    
    aadharID = data['aadharID']
    password = data['password']

    if True:
    	res = {
    		"status" : "success"
    	}
    	return jsonify(res)
    else:
    	res = {
    		"status" : "failed",
    		"message" : "Something went wrong, cannot register the user"
    	}
    	return jsonify(res)

# Login - Get Credentioals and Return User Information
@api.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    
    aadharID = data['aadharID']
    password = data['password']

    if True:
        if True:
            res = {
                "status" : "success"
            }
            return jsonify(res)
        else:
        res = {
            "status" : "failed",
            "message" : "Incorrect Password"
        }
        return jsonify(res)
    else:
        res = {
            "status" : "failed",
            "message" : "Aadhar not Registered"
        }
        return jsonify(res)


# CheckNotification - Check If user has any new notification
@api.route('/checkNotification', methods=['GET', 'POST'])
def checkNotification():
    data = request.get_json()
    if True:
    	res = {
    		"status" : "success",
    		"type" : "success",	# success, warning or danger
    		"body" : "message body",
    		"link" : "http://google.com"
    	}
    	return jsonify(res)
    else:
    	res = {
    		"status" : "failed",
    		"message" : "No New Notification"
    	}
    	return jsonify(res)

# Run
if __name__ == '__main__':
    api.run()
