# TellMe
Application to collect and analyze Irrigation Data.

## Demo
[Demo Link](https://quiet-sierra-48529.herokuapp.com)

**Username:** `111111111111`

**Password:** `demo1234`


## About

It's an application to collect and analyze the irrigation data to reduce water wastage. It solves the problem in three major steps. Collect. Analyze. Connect.

**Collect** - It starts with the collection of the data. The Irrigation data can be collected with the help of Mobile Application. It is stored in OLTP Database. Both communicate with the help of REST APIs.

**Analyze** - In this phase the collected data is then migrated to OLAP Database. After the migration the data can be exported in the desired format to analyze. The administrators can export the data from the Web Portal. After that, they can analyze the data with the help of advance tools and get the insights.

**Connect** - The insights and relevant information can be shared with the farmers and irrigation authorities. 

### Version
0.5

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


**/api/login :**
```sh
	{
		"aadharID":"",
		"password":""
	}
```


**/api/checkNotification :**
```sh
	{
		"aadharID":"",
	}
```


**/api/feedFarmData :**
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
