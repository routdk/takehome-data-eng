CREATE TABLE IF NOT EXISTS current_weather_history  (
	city_name VARCHAR(255),
	longitude NUMERIC NOT NULL,
	latitude NUMERIC NOT NULL,
	weather_description TEXT[],
    current_temperature NUMERIC,
    feels_like_temperature NUMERIC,
    pressure NUMERIC,
    humidity NUMERIC,
    temp_min NUMERIC,
    temp_max NUMERIC,
    atm_pressure_sea_level NUMERIC,
    atm_pressure_grnd_level NUMERIC,
    visibility_mtr NUMERIC,
    wind_speed NUMERIC,
    wind_direction NUMERIC,
    wind_gust NUMERIC,
    pct_cloudiness NUMERIC,
    rain_last_1hr NUMERIC,
    rain_last_3hr NUMERIC,
    snow_last_1hr NUMERIC,
    snow_last_3hr NUMERIC,
    country_code VARCHAR(255),
    sunrise_time_utc TIMESTAMPTZ,
    sunset_time_utc TIMESTAMPTZ,
    timezone_shift_secs_from_utc NUMERIC,
    data_timestamp_utc TIMESTAMPTZ
);



