"""
Ideally its a good idea to de-couple the data extraction, processing and loading
into multiple tasks. But in this DAG I have coupled them together for the below
reasons.
- We don't have access to a cloud storage at hand to persist the extracted records.
- Data transfer between tasks in airflow is non trivial. xcom push a way to transfer on-the-fly data. 

So I have removed couple of TO-DOs and adjusted it based on solution approach. 
"""

import time
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from utils.load_env import get_env_secrets
from utils.openweather_utils import (
    fetch_current_weather_by_geo_coord,
    current_weather_data_flatten,
    postgres_db_connection,
    postgres_table_insert,
)
from utils.process_master_list import create_master_coordinates

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
with DAG(
    "fetcher",
    default_args=default_args,
    description="To fetch the weather data",
    schedule_interval=timedelta(minutes=60),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["take-home"],
) as dag:

    def etl_prcessing():
        """Extract,transform and Load coupled together"""
        master_coordinates = create_master_coordinates()
        for coordinates in master_coordinates:
            data = fetch_current_weather_by_geo_coord(**coordinates)
            flattened_data = current_weather_data_flatten(data)
            postgres_conn = postgres_db_connection(
                postgres_host=get_env_secrets("postgres_host"),
                postgres_db=get_env_secrets("postgres_db"),
                postgres_user=get_env_secrets("postgres_user"),
                postgres_password=get_env_secrets("postgres_password"),
                postgres_db_port=get_env_secrets("postgres_db_port"),
            )
            postgres_table_insert(
                postgres_connection=postgres_conn,
                table_name="current_weather_history",
                parsed_rec=flattened_data,
            )

    t1 = PostgresOperator(
        task_id="create_table",
        sql="sql/current_weather_history_ddl.sql",
        postgres_conn_id="weather_db_postgres",
    )
    t2 = PythonOperator(
        task_id="ingest_api_raw_data",
        python_callable=etl_prcessing,
    )

    t1 >> t2
