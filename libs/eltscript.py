import datetime as dt

lastUpdated = dt.date(2000,1,1)  # last updated global variable
def prepareDB():
	import psycopg2 as pg2
	import datetime as dt
	import psycopg2.extras as pgext

	connfrom = pg2.connect(database="d1g2c8ihf7qeng",user="ucyteulerrxxoo",password="bca5e14e8dcc20b2a4bcb4bee2227e5b44cc02f488fba40240d1764c4ac750ca",host="ec2-23-21-217-27.compute-1.amazonaws.com",port="5432")
	connfrom.set_session(readonly=True)
	connto = pg2.connect(database="db70oouohkh4bj",user="fnqryfoivwpuxd",password="884e1a40af2227d023c58401914873dfea4d44530a34647bb5930872b1a21807",host="ec2-54-221-220-59.compute-1.amazonaws.com",port="5432")


	curfrom = connfrom.cursor(cursor_factory=pgext.DictCursor)
	curto = connto.cursor()

	curfrom.execute('''select * from farm as f, crop as c, irrigation as i, weather as w
		                where f.farm_id=c.farm_id and c.crop_id=i.crop_id and i.irrigation_date=w.weather_date
		                and i.irrigation_date > %s''', (lastUpdated,))

	for i in curfrom.fetchall():
		curto.execute('''select farm_id from location_dim where farm_id=%s''', (i['farm_id'],))
		farm_id = curto.fetchone()
		if farm_id == None:
		    curto.execute('''insert into location_dim(farm_id, area_id, longitude, latitude,
		                sub_area_size, land_area, soil_type, geo_area_code, state,
		                 district, city) values
		                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
		                (i['farm_id'], i['crop_id'], i['longitude'], i['latitude'],
		                i['crop_seeded_area_size'], i['land_area'], i['soil_type'],
		                i['geo_area_code'], i['state'], i['district'], i['city']))


		curto.execute('''select crop_id from crop_dim where crop_name=%s and seed_id=%s ''',
		                (i['crop_name'], i['seed_id']))
		crop_id = curto.fetchone()
		if  crop_id == None:
		    curto.execute('''insert into crop_dim(crop_name, seed_id) values
		                (%s, %s)''', (i['crop_name'], i['seed_id']))

		curto.execute('''select weather_id from weather_dim where weather_date=%s and
		            geo_area_code=%s''', (i['weather_date'], i['geo_area_code']))
		weather_id = curto.fetchone()
		if weather_id == None:
		    curto.execute('''insert into weather_dim(weather_date, geo_area_code,
		                temperature, humidity, precipitation) values
		                (%s, %s, %s, %s, %s)''',(i['weather_date'], i['geo_area_code'],
		                i['temperature'], i['humidity'], i['precipitation']))
		curto.execute('''select farm_id from location_dim where farm_id=%s''',
		            (i['farm_id'],))
		location_id = curto.fetchone()

		curto.execute('''select crop_id from crop_dim where crop_name=%s and
		                seed_id=%s''', (i['crop_name'], i['seed_id']))
		crop_id = curto.fetchone()

		curto.execute('''select weather_id from weather_dim where weather_date=%s
		            and geo_area_code=%s''', (i['irrigation_date'], i['geo_area_code']))
		weather_id = curto.fetchone()
		[print(i, ' : ', type(i)) for i in [location_id[0], weather_id[0],  crop_id[0], i['water_source'],
		i['water_source'], i['data_source'], i['irrigation_date'],
		i['water_amount']]]
		curto.execute('''insert into fact_table(location_id, crop_id, weather_id,
		                water_source, data_source, water_amount, irrigation_date)
		                values (%s, %s, %s, %s, %s, %s, %s)''',
		                (location_id[0], crop_id[0], weather_id[0],
		                i['water_source'], i['data_source'], i['water_amount'],
		                i['irrigation_date']))
		# print(list(i.keys()), '\n\n')
	connto.commit()
	connto.close()
	connfrom.close()
	# curto.close()
	# curfrom.close()
	lastUpdated = datetime.date.today()
	
	
	
	

