with temperature_data_cte
as
(
select 
city_name,
current_temperature,
feels_like_temperature,
date(date_trunc('day', data_timestamp_utc))  as date
from current_weather_history
-- Let's scope the rows to 5 cities in USA
where city_name in 
('San Francisco','Seattle','Dallas','New York City','Boston')
and date(date_trunc('day', data_timestamp_utc)) >= 
    coalesce((select max(date) from city_day_summary_temerature),'1900-01-01')
),
temperature_data_transformed_cte as
(
select 
city_name,
date, 
min(current_temperature) as min_temp, 
max(current_temperature) as max_temp,
min(feels_like_temperature) as min_feels_like_temp, 
max(feels_like_temperature) as max_feels_like_temp,
avg(current_temperature) as avg_temp, 
avg(feels_like_temperature) as avg_feels_like_temp,
now() as etl_insert_date
from temperature_data_cte
group by city_name, date
)
INSERT INTO city_day_summary_temerature 
(
city_name, 
date, 
min_temp, 
max_temp, 
min_feels_like_temp,
max_feels_like_temp,
avg_temp,
avg_feels_like_temp,
etl_insert_date
)
select city_name, date, min_temp, max_temp, min_feels_like_temp, max_feels_like_temp, avg_temp, avg_feels_like_temp, etl_insert_date  
from temperature_data_transformed_cte
where not exists (
select * from city_day_summary_temerature
where city_day_summary_temerature.city_name = temperature_data_transformed_cte.city_name 
and city_day_summary_temerature.date = temperature_data_transformed_cte.date 
)
on conflict (city_name, date)
do update set
	min_temp = EXCLUDED.min_temp,
    max_temp = EXCLUDED.max_temp,
    min_feels_like_temp = EXCLUDED.min_feels_like_temp,
    max_feels_like_temp = EXCLUDED.max_feels_like_temp,
    avg_temp = EXCLUDED.avg_temp,
    avg_feels_like_temp = EXCLUDED.avg_feels_like_temp,
    etl_insert_date = EXCLUDED.etl_insert_date;
    
