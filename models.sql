CREATE TABLE users (
	aadhar_id VARCHAR(12) PRIMARY KEY,
	password TEXT,
	name TEXT,
	contact_no TEXT,
	user_type VARCHAR(20) DEFAULT 'FARMER',
	message_broadcast hstore
);

CREATE TABLE farm (
	farm_id BIGSERIAL PRIMARY KEY,
	farm_name TEXT,

	belongs_to REFERENCES users(aadhar_id),

	farm_registration_date DATE DEFAULT now()::DATE,
	farm_status BOOLEAN DEFAULT TRUE,

	geo_area_code TEXT,
	longitude DECIMAL(10,7),
	latitude DECIMAL(10,7),
	state TEXT,
	district TEXT,
	city TEXT,

	land_area REAL,
	groundwater_level REAL,

	soil_type TEXT
);

CREATE TABLE crop (
	crop_id BIGSERIAL PRIMARY KEY,
	crop_name TEXT,

	belongs_to REFERENCES users(aadhar_id),
	farm_id REFERENCES farm(farm_id),

	seed_id TEXT,

	crop_seeded_on DATE DEFAULT now()::DATE,
	crop_seeded_area_size REAL,

	crop_status BOOLEAN DEFAULT TRUE
);

CREATE TABLE weather (
	weather_date DATE DEFAULT now()::DATE,
	geo_area_code TEXT,
	temperature TEXT,
	humidity TEXT,
	precipitation TEXT,
);

CREATE TABLE irrigation(
	crop_id REFERENCES crop(crop_id),
	irrigation_date DATE DEFAULT now()::DATE,
	geo_area_code TEXT,

	water_amount REAL,
	water_source TEXT,
	data_source TEXT DEFAULT 'ANDROID'
);
