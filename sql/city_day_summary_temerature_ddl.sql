CREATE TABLE IF NOT EXISTS city_day_summary_temerature  (
	city_name VARCHAR(255) NOT NULL,
	date TIMESTAMPTZ NOT NULL,
    min_temp NUMERIC,
    max_temp NUMERIC,
    min_feels_like_temp NUMERIC,
    max_feels_like_temp NUMERIC,
    avg_temp NUMERIC,
    avg_feels_like_temp NUMERIC,
    etl_audit_date TIMESTAMPTZ
);

ALTER TABLE city_day_summary_temerature
DROP CONSTRAINT IF EXISTS unique_key_city_date;

ALTER TABLE city_day_summary_temerature
ADD CONSTRAINT unique_key_city_date UNIQUE (city_name, date);


