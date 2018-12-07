# TellMe
Application to collect and analyze Irrigation Data.

### Version
0.2

## Usage

### Clone
Clone the Project

```sh
$ git clone https://github.com/JitendraNirnejak/TellMe.git
$ cd TellMe
```

### Installation

Install the dependencies (flask, psycopg etc.)

```sh
$ pipenv install
```

### Run

This will start the server

```sh
$ python app.py
```

## API Endpoints:

POST the given data in JSON format

**/api/getOTP :**
```sh
	{
		"aadharID": ""
	}
```


**/api/verifyOTP :**
```sh
	{
		"aadharID":"",
		"OTP":""
	}
```


**/api/register :**
```sh
	{
		"aadharID":"",
		"password":"",
		"contactNo":"",
		"name":""
	}
```


### **/api/login :**
```sh
	{
		"aadharID":"",
		"password":""
	}
```


### **/api/checkNotification :**
```sh
	{
		"aadharID":"",
	}
```


### **/api/feedFarmData :**
```sh
	{
		"aadharID":"",
		"farmName":"",
		"longitude":"",
		"latitude":"",
		"state":"",
		"district":"",
		"city":"",
		"landArea":"",
		"groundWaterLevel":"",
		"soilType":""
	}
```


**/api/getFarmList :**
```sh
	{
		"aadharID":""
	}
```

**/api/feedCropData :**
```sh
	{
		"aadharID":""
	}
```

**/api/getCropList :**
```sh
	{
		"aadharID":""
	}
```

**/api/feedIrrigationData :**
```sh
	{
		"aadharID":""
	}
```


**Common Format of Response :**
```sh
	{
		"status":"success"
	}
```
```sh

	{
		"status" : "failed",
		"message" : "Something went wrong"
	}
```
