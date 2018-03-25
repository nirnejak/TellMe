# Librarys
from flask import request
from flask import jsonify

import psycopg2 as pg2

# Importing the Application Modules
from app import app
from data import aadharData


# Connecting to database
conn = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")


# Views

# GetOTP - Return Success Message if aadhar ID is valid and unregistered
@app.route('/api/getOTP', methods=['GET', 'POST'])
def getOTP():
    res={}
    if request.method == 'POST':
        # Receiving Aadhar ID
        aadharID = request.get_json()['aadharID']
        
        if len(aadharID)==12 and aadharID in aadharData:
            # Creating cursor
            cur = conn.cursor()
            
            # Executing Query
            try:
                cur.execute("SELECT aadhar_id FROM user_all WHERE aadhar_id = %s",[aadharID])
            except:
                conn.rollback()
                res = {
                    "status" : "failed",
                    "message" : "Something went wrong"
                }
                return jsonify(res)

            # Fetching Data
            data = cur.fetchall()

            if data:
                res = {
                    "status" : "failed",
                    "message" : "Aadhar ID is already registered"
                }
            else:
                # Generating Response
                res = {
                    "status" : "success"
                }

            # Commiting the Changes
            conn.commit()

            # Closing the cursor
            cur.close()
        else:
            res = {
                "status" : "failed",
                "message" : "Incorrect Aadhar ID"
            }
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }

    return jsonify(res)

# verifyOTP - Return Success Message if OTP sent by the user is correct
@app.route('/api/verifyOTP', methods=['GET', 'POST'])
def verifyOTP():
    if request.method == 'POST':
        data = request.get_json()
        res = {}
    
        aadharID = data["aadharID"]
        OTP = data["OTP"]

        if OTP=='123456':
            res = {
                "status" : "success"
            }
        else:
            res = {
                "status" : "failed",
                "message" : "Incorrect OTP"
            }
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)

# Register - Register the User and send Success Message
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        aadharID = data['aadharID']
        password = data['password']

        # Fetching from Aadhar
        contactNo = aadharData[aadharID]['contact_no']
        name = aadharData[aadharID]['name']

        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("INSERT INTO user_all VALUES(%s,%s,%s,%s,%s)",[aadharID, password, name, contactNo,'REGISTERED'])
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        # Generate Response
        res = {
            "status" : "success"
        }

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }

    return jsonify(res)

# Login - Get Credentioals and Return User Information
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        
        aadharID = data['aadharID']
        password_candidate = data['password']

        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("SELECT password,user_status,name FROM user_all WHERE aadhar_id = %s",[aadharID])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)

        # Generate Response
        data = cur.fetchone()

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

        if data:
            # Compare Passwords
            if password_candidate == data[0]:
                res = {
                    "status" : "success",
                    "aadharID" : aadharID,
                    "name" : data[2],
                    "userStatus" : data[1]
                }
            else:
                res = {
                    "status" : "failed",
                    "message" : "Invalid Login"
                }
        else:
                res = {
                    "status" : "failed",
                    "message" : "Aadhar not Registered"
                }
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)





# CheckNotification - Check If user has any new notification
@app.route('/api/checkNotification', methods=['GET', 'POST'])
def checkNotification():
    if request.method == 'POST':
        data = request.get_json()

        aadharID = data['aadharID']
        
        if True:
        	res = {
        		"status" : "success",
        		"type" : "success",	# success, warning or danger
        		"body" : "message body",
        		"link" : "http://google.com"
        	}
        else:
        	res = {
        		"status" : "failed",
        		"message" : "No New Notification"
        	}
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)

# Feed Farm Data
@app.route('/feedFarmData', methods=['GET', 'POST'])
def feedFarmData():
    if request.method == 'POST':
        data = request.get_json()
        res = data

        '''
        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        
        try:
            cur.execute("%s",[aadharID])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)
        
        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

        res = {
            "status" : "success"
        }
        '''
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)

# Get Farm List - Return List of Farms associated to a particular user
@app.route('/getFarmList', methods=['GET', 'POST'])
def getFarmList():
    if request.method == 'POST':
        data = request.get_json()
        # Get aadharID
        aadharID = data["aadharID"]

        '''
         # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("%s",[aadharID])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)

        # Generate Response
        data = cur.fetchone()

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()
        '''
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)

# Feed Crop Details
@app.route('/feedCropData', methods=['GET', 'POST'])
def feedCropData():
    if request.method == 'POST':
        data = request.get_json()
        res = data
        '''
         # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("%s",[aadharID])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)

        # Generate Response
        data = cur.fetchone()

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

        '''
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)
# Get Crop List - Return List of Crops associated to a particular user
@app.route('/getCropList', methods=['GET', 'POST'])
def getCropList():
    if request.method == 'POST':
        data = request.get_json()
        res = data
        '''
        # Get aadharID
        aadharID = data["aadharID"]

         # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("SELECT crop_id, crop_name, crop_info FROM crops WHERE aadhar_is = %s",[aadharID])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)

        # Generate Response
        data = cur.fetchone()

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()
        '''
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)

# Feed Irrigation Details
@app.route('/feedIrrigationData', methods=['GET', 'POST'])
def feedIrrigationData():
    if request.method == 'POST':
        data = request.get_json()
        res = data

        '''
         # Get aadharID
        aadharID = data["aadharID"]

         # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("SELECT crop_id, crop_name, crop_info FROM crops WHERE aadhar_is = %s",[aadharID])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)

        # Generate Response
        data = cur.fetchone()

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()
        '''
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)