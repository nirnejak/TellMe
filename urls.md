## URLs

API:

##/api/getOTP
	Input:
		{
			"aadharID": ""
		}


#/api/verifyOTP
	Input:
		{
			"aadharID":"",
			"OTP":""
		}


#/api/register
	Input:
		{
			"aadharID":"",
			"password":"",
			"contactNo":"",
			"name":""
		}


#/api/login
	Input:
		{
			"aadharID":"",
			"password":""
		}


#/api/checkNotification
	Input:
		{
			"aadharID":""
		}


#/api/feedFarmData
		{
			"aadharID":""
		}


#/api/getFarmList
		{
			"aadharID":""
		}

#/api/feedCropData
		{
			"aadharID":""
		}

#/api/getCropList
		{
			"aadharID":""
		}

#/api/feedIrrigationData
		{
			"aadharID":""
		}





#Common Format of Output

	{
		"status":"success"
	}

	{
		"status" : "failed",
		"message" : "your life sucks"
	}