# Librarys
from flask import request
from flask import jsonify

import psycopg2 as pg2
import psycopg2.extras as pgext
# Importing the Application Modules
from app import app

# Importing Personal Libraries  


from libs.geo_area_code import find_geo_area_code
from libs.data import aadharData


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
                cur.execute("SELECT aadhar_id FROM users WHERE aadhar_id = %s;",[aadharID])
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
                    "status" : "success",
                    "contactNo" : aadharData[aadharID]['contact_no']
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
        try:
            contactNo = aadharData[aadharID]['contact_no']
            name = aadharData[aadharID]['name']
        except:
            res = {
                "status" : "failed",
                "message" : "Invalid Aadhar ID"
            }
            return jsonify(res)

        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("INSERT INTO users(aadhar_id,password,name,contact_no) VALUES(%s,%s,%s,%s);",[aadharID, password, name, contactNo])
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
        cur = conn.cursor(cursor_factory=pgext.DictCursor)
        # Executing Query
        try:
            cur.execute("SELECT password, name, message_broadcast FROM users WHERE aadhar_id = %s  AND user_type = 'FARMER';",[aadharID])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)

        # Generate Response
        dataRecieved = cur.fetchone()

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

        if data:
            # Compare Passwords
            if password_candidate == dataRecieved['password']:
                res = {
                    "status" : "success",
                    "aadharID" : aadharID,
                    "name" : dataRecieved['name'],
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
        
        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("SELECT message_broadcast FROM users WHERE aadhar_id = %s AND user_type = 'FARMER';",[aadharID])
        except:
            conn.rollback()
            res["status"]="failed"
            res['message']="Something went wrong"
            return jsonify(res)

        # Generate Response
        data = cur.fetchone()

        # Closing the cursor
        cur.close()

        if data:
        	res = {
        		"status" : "success",
        		"type" : data["type"],	# success, warning or danger
        		"body" : data["body"],
        		"link" : data["link"]
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
@app.route('/api/feedFarmData', methods=['GET', 'POST'])
def feedFarmData():
    if request.method == 'POST':
        data = request.get_json()

        # Getting Data
        farmName = data['farmName']
        belongs_to = data['aadharID']
        longitude = float(data['longitude'])
        latitude = float(data['latitude'])
        geoareaCode = find_geo_area_code(longitude, latitude)
        state = data['state']
        district = data['district']
        city = data['city']
        landArea = data['landArea']
        groundWaterLevel = data['groundWaterLevel']
        soilType = data['soilType']

        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        
        try:
            cur.execute("INSERT INTO farm(farm_name, belongs_to, geo_area_code, longitude, latitude, state, district, city, land_area, groundwater_level, soil_type) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",(farmName, belongs_to, geoareaCode, longitude, latitude, state, district, city, landArea, groundWaterLevel, soilType))
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong",
            }
            return jsonify(res)
        
        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

        res = {
            "status" : "success"
        }

    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)

# Get Farm List - Return List of Farms associated to a particular user
@app.route('/api/getFarmList', methods=['GET', 'POST'])
def getFarmList():
	if request.method == 'POST':
		data = request.get_json()
		# Get aadharID
		aadharID = data["aadharID"]

		# Creating cursor
		cur = conn.cursor(cursor_factory = pgext.DictCursor)
		# Executing Query
		try:
			cur.execute("SELECT farm_id, farm_name FROM farm WHERE belongs_to = %s",[aadharID])
		except:
			conn.rollback()
			res = {
				"status" : "failed",
				"message" : "Something went wrong"
			}
			return jsonify(res)

		# Generate Response
		data = cur.fetchall()
		
		if data:
			res = {
				"status" : "success",
				"data" : []
			}
			for i in data:
				res["data"].append({"farmID" : i['farm_id'], "farmName" : i['farm_name']})
		else:
			res = {
				"status" : "failed",
				"message" : "you don't have any farm"
			}
		# Closing the cursor
		cur.close()
	else:
		res = {
			"status" : "failed",
			"message" : "Invalid Request Method"
		}
	return jsonify(res)

# Feed Crop Details
@app.route('/api/feedCropData', methods=['GET', 'POST'])
def feedCropData():
    if request.method == 'POST':
        data = request.get_json()

        cropName = data['cropName']
        aadharID = data['aadharID']
        farmID = data['farmID']
        seedID = data['seedID']
        cropSeededAreaSize = data['cropSeededAreaSize']

         # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("INSERT INTO crop(crop_name,belongs_to,farm_id,seed_id,crop_seeded_area_size) values(%s,%s,%s,%s,%s)",(cropName,aadharID,farmID,seedID,cropSeededAreaSize))
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

        # Generating Response
        res = {
            "status" : "success"
        }
        
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)
# Get Crop List - Return List of Crops associated to a particular user
@app.route('/api/getCropList', methods=['GET', 'POST'])
def getCropList():
    if request.method == 'POST':
        data = request.get_json()
       
        # Get aadharID
        aadharID = data["aadharID"]

         # Creating cursor
        cur = conn.cursor(cursor_factory=pgext.DictCursor)
        # Executing Query
        try:
            cur.execute("SELECT crop_id, crop_name FROM crop WHERE belongs_to = %s",[aadharID])
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        # Generate Response
        data = cur.fetchall()

        if data:
            res = {
                "status" : "success",
                "data" : []
            }
            for i in data:
                res["data"].append({ "cropID" : i['crop_id'], "cropName" : i['crop_name']})
        else:
            res = {
                "status":"failed",
                "message":"You don't have any Crops"
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

# Feed Irrigation Details
@app.route('/api/feedIrrigationData', methods=['GET', 'POST'])
def feedIrrigationData():
    if request.method == 'POST':
        data = request.get_json()

        cropID = data['cropID']
        waterAmount = data['waterAmount']
        waterSource = data['waterSource']

         # Creating cursor
        cur = conn.cursor()
        
        # Executing Query
        try:
            cur.execute("INSERT into irrigation(crop_id,water_amount,water_source) values(%s,%s,%s)",(cropID,waterAmount,waterSource))
        except:n
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        # Commiting the Changes
        conn.commit()

        # Closing the cursor
        cur.close()

        res = {
            "status" : "success"
        }
        
    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)