import sys
from datetime import datetime
from typing import Optional, Union
import time
import requests
from psycopg2 import connect, sql
from psycopg2.extensions import connection

from utils.load_env import get_env_secrets

OPENWEATHERMAP_APIKEY = get_env_secrets("openweathermap_apikey")
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_QUERY_PARAMS = {"units": "imperial", "appid": f"{OPENWEATHERMAP_APIKEY}"}


def fetch_current_weather_by_geo_coord(
    *, lat: Union[int, float], lon: Union[int, float]
) -> dict:
    """Returns current weather attributes as a dict based on lat, long"""
    try:
        api_query = {**DEFAULT_QUERY_PARAMS, "lat": lat, "lon": lon}
        response = requests.get(API_ENDPOINT, params=api_query)
        if response.status_code == 429:
            time.sleep(int(response.headers["Retry-After"]))
        response.raise_for_status()

    except (
        requests.exceptions.HTTPError,
        requests.exceptions.TooManyRedirects,
        requests.ConnectionError,
        requests.Timeout,
    ) as error:
        print(error)
        sys.exit(1)
    return response.json()


def current_weather_data_flatten(api_output: dict) -> dict:
    """Flatten data and keep only field needed.
    After closely inspecting the output of the dictionary 3 patterns are visible.
    1. Single level nesting.
    2. Two level nesting.
    3. Single level nesting with a list as value.
    So here are the functions to retrive the value in order to flatten
    the dict (nested ones as we don't plan them to use outside of this
    function really)
    """

    def get_dict_value_1_level_nesting(first_key: str) -> Optional[str]:
        return api_output.get(first_key)

    def get_dict_value_2_level_nesting(
        first_key: str, second_key: str
    ) -> Optional[str]:
        return (api_output.get(first_key) or {}).get(second_key)

    def get_weather_desc() -> Optional[list]:
        weather_details = api_output.get("weather")
        if weather_details and isinstance(weather_details, list):
            desc_list = [weather.get("description") for weather in weather_details]
        return desc_list

    def unixtime_to_date_format(epoch_time: int) -> Optional[str]:
        """Convert epoch time to string formatted datetime"""
        return (
            datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%d %H:%M:%S")
            if epoch_time is not None
            else None
        )

    parsed_result = {}
    column_transformation_mapping = {
        "city_name": get_dict_value_1_level_nesting("name"),
        "longitude": get_dict_value_2_level_nesting("coord", "lon"),
        "latitude": get_dict_value_2_level_nesting("coord", "lat"),
        "weather_description": get_weather_desc(),
        "current_temperature": get_dict_value_2_level_nesting("main", "temp"),
        "feels_like_temperature": get_dict_value_2_level_nesting("main", "feels_like"),
        "pressure": get_dict_value_2_level_nesting("main", "pressure"),
        "humidity": get_dict_value_2_level_nesting("main", "humidity"),
        "temp_min": get_dict_value_2_level_nesting("main", "temp_min"),
        "temp_max": get_dict_value_2_level_nesting("main", "temp_max"),
        "atm_pressure_sea_level": get_dict_value_2_level_nesting("main", "sea_level"),
        "atm_pressure_grnd_level": get_dict_value_2_level_nesting("main", "grnd_level"),
        "visibility_mtr": get_dict_value_1_level_nesting("visibility"),
        "wind_speed": get_dict_value_2_level_nesting("wind", "speed"),
        "wind_direction": get_dict_value_2_level_nesting("wind", "deg"),
        "wind_gust": get_dict_value_2_level_nesting("main", "gust"),
        "pct_cloudiness": get_dict_value_2_level_nesting("clouds", "all"),
        "rain_last_1hr": get_dict_value_2_level_nesting("rain", "1h"),
        "rain_last_3hr": get_dict_value_2_level_nesting("rain", "3h"),
        "snow_last_1hr": get_dict_value_2_level_nesting("snow", "1h"),
        "snow_last_3hr": get_dict_value_2_level_nesting("snow", "3h"),
        "country_code": get_dict_value_2_level_nesting("sys", "country"),
        "sunrise_time_utc": unixtime_to_date_format(
            get_dict_value_2_level_nesting("main", "sunrise")
        ),
        "sunset_time_utc": unixtime_to_date_format(
            get_dict_value_2_level_nesting("main", "sunset")
        ),
        "timezone_shift_secs_from_utc": get_dict_value_1_level_nesting("timezone"),
        "data_timestamp_utc": unixtime_to_date_format(
            get_dict_value_1_level_nesting("dt")
        ),
    }
    for field, transformation in column_transformation_mapping.items():
        parsed_result[field] = transformation

    return parsed_result


def postgres_db_connection(
    *,
    postgres_host: str,
    postgres_db: str,
    postgres_user: str,
    postgres_password: str,
    postgres_db_port: str,
) -> connection:

    """Creates a postgres connection object"""
    try:
        return connect(
            host=postgres_host,
            database=postgres_db,
            user=postgres_user,
            password=postgres_password,
            port=postgres_db_port,
        )

    except Exception as error:
        print(error)
        sys.exit(1)


def postgres_table_insert(
    *, postgres_connection, table_name: str, parsed_rec: dict
) -> None:
    """Generate insert statements for postgres"""
    fields = list(parsed_rec.keys())
    val = tuple([parsed_rec[field] for field in fields])

    with postgres_connection.cursor() as cursor:
        postgres_connection.autocommit = True
        ## https://stackoverflow.com/questions/61341246/psycopg2-dynamic-insert-query-issues-syntax-error-at-or-near-identifier
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
            sql.Identifier(table_name),
            sql.SQL(",").join(map(sql.Identifier, fields)),
            sql.SQL(",").join(sql.Placeholder() * len(fields)),
        )
        cursor.execute(query, val)
        cursor.close()
