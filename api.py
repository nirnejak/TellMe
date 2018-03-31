# Librarys
from flask import request
from flask import jsonify
from datetime import timedelta 
import logging
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
    import datetime as dt
    if request.method == 'POST':
        data = request.get_json()

        aadharID = data['aadharID']
        
        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("SELECT irrigation_date FROM irrigation WHERE aadhar_id = %s ORDER BY irrigation_date DESC LIMIT 1;",[aadharID])
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        conn.commit()
        # Generate Response
        data = cur.fetchone()[0]

        try:
            if data + dt.timedelta(7) < dt.date.today():
                cur.execute('SELECT reward_point FROM rewards WHERE aadhar_id = %s;',[aadharID])
                reward = cur.fetchone()[0]
                conn.commit()

                cur.execute('UPDATE rewards SET reward_point = %s;',[reward+1])
                conn.commit()

                cur.execute('UPDATE rewards SET last_reward_date = %s;',[dt.date.today()])
                conn.commit()

                res = {
                    "reward" :reward+1
                }
                return jsonify(res)
            else:
                cur.execute('SELECT reward_point FROM rewards WHERE aadhar_id = %s;',[aadharID])
                reward = cur.fetchone()[0]
                conn.commit()
                res = {
                   "reward" :reward
                }
                return jsonify(res)    

            # app.logger.info("mayab")
                
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went very wrong"
            }
            return jsonify(res)
        
        # Closing the cursor
        cur.close()

    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)


@app.route('/api/tempRoute', methods=['GET', 'POST'])
def checkMessage():
    if request.method == 'POST':
        data = request.get_json()

        aadharID = data['aadharID']
        
        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("SELECT message_broadcast from users where aadhar_id = %s",[aadharID])
            data = cur.fetchone()[0]
            conn.commit()
            if data != None :
            	res = {
            		"notification" : data
            	} 
            	return jsonify(res)
            else:
            	res = {
            		"notification": ""
            	}	
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        conn.commit()
        # Generate Response
                
      	# Closing the cursor
        cur.close()

    else:
        res = {
            "status" : "failed",
            "message" : "Invalid Request Method"
        }
    return jsonify(res)


@app.route('/api/clearMessage', methods=['GET', 'POST'])
def clearMessage():
    if request.method == 'POST':
        data = request.get_json()

        aadharID = data['aadharID']
        
        # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("UPDATE users set message_broadcast = ''",[aadharID])
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        conn.commit()
        # Generate Response
                
      	# Closing the cursor
        cur.close()

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
        season = data['season']

         # Creating cursor
        cur = conn.cursor()
        # Executing Query
        try:
            cur.execute("INSERT INTO crop(crop_name,belongs_to,farm_id,seed_id,crop_seeded_area_size,season) values(%s,%s,%s,%s,%s,%s)",(cropName,aadharID,farmID,seedID,cropSeededAreaSize,season))
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
        aadharID = data['aadharID']

         # Creating cursor
        cur = conn.cursor()
        
        # Executing Query
        try:
            cur.execute("INSERT into irrigation(crop_id,water_amount,water_source,aadhar_id) values(%s,%s,%s,%s)",(cropID,waterAmount,waterSource,aadharID))
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        # Commiting the Changes
        conn.commit()
        try:
             cur.execute("SELECT crop_seeded_area_size,crop_name from crop where crop_id = %s;",[cropID]) 
        except:
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went wrong"
            }
            return jsonify(res)

        temp = cur.fetchone()
        farmer_seeded_area = temp[0]
        cropName = temp[1]
        # res = {
        #     "data" : farmer_seeded_area,
        #     "water": waterAmount
        # }
        # return jsonify(res)

        # Commiting the Changes
        conn.commit()
        waterAmountPerDay = int(waterAmount) * farmer_seeded_area
        res = {
            "water": waterAmountPerDay
        }
        

        try:
            cur.execute("SELECT crop_name,water_amount_per_sq_m from required_water_amount where crop_name= %s;",[cropName]) 
            temp = cur.fetchall()
            
            cropName_required = temp[0][0]
            waterAmount_required = temp[0][1] * farmer_seeded_area
            res = {
            "name" : temp,
            "cropName": cropName,
            "crop_name": cropName_required,
            "water": waterAmount_required
            }
            
        except:      
            conn.rollback()
            res = {
                "status" : "failed",
                "message" : "Something went not wrong"
            }
        
        # Commiting the Changes
        conn.commit()
        try:
            if (waterAmountPerDay - waterAmount_required) > 5 :
                message = 'You are using excess amount of water for the crop, please control your water usage.'
                res = {
                    "data": message,
                    "aadharID" : aadharID
                }
                # return jsonify(res)
                cur.execute("UPDATE users set message_broadcast = %s where aadhar_id = %s;",(message,aadharID))

        except:      
            conn.rollback()

            res = {
                "status" : "failed",
                "message" : "Something went very wrong"
            }
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
