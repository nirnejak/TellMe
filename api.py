# Librarys
from flask import request
from flask import jsonify

import psycopg2 as pg2
from passlib.hash import sha256_crypt

# Importing the Application Modules
from app import app

# Views

# GetOTP - Return Success Message if aadhar ID is valid and unregistered
@app.route('/api/getOTP', methods=['GET', 'POST'])
def getOTP():
    res={}
    if request.method == 'POST':
        # Receiving Aadhar ID
        aadharID = request.get_json()['aadharID']
        
        if len(aadharID)==12:
            # Connecting to database
            conn = pg.connect(database="",user="",password="",host="",port="5432")
            # Creating cursor
            cur = conn.cursor()
            # Executing Query
            cur.execute("SELECT * FROM users WHERE aadharID = %s",[aadharID])

            # Generating Response
            res["status"]="success"

            # Commiting the Changes
            conn.commit()

            # Closing the connection
            conn.close()
        else:
            res["status"]="failed"
            res['message']="Incorrect Aadhar ID"
    else:
        res["status"]="failed"
        res['message']='Invalid Request Method'

    return jsonify(res)

# verifyOTP - Return Success Message if OTP sent by the user is correct
@app.route('/api/verifyOTP', methods=['GET', 'POST'])
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
@app.route('/api/register', methods=['GET', 'POST'])
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
@app.route('/api/login', methods=['GET', 'POST'])
def login():
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
@app.route('/api/checkNotification', methods=['GET', 'POST'])
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