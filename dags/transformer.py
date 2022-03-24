from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.providers.postgres.operators.postgres import PostgresOperator

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
with DAG(
    "transformer",
    default_args=default_args,
    description="To transform the raw current weather to a modeled dataset",
    schedule_interval="@daily",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    template_searchpath=["/opt/airflow/sql"],
    tags=["take-home"],
) as dag:

    t1 = PostgresOperator(
        task_id="create_agg_table_city_day_summary_temerature",
        sql="city_day_summary_temerature_ddl.sql",
        postgres_conn_id="weather_db_postgres",
    )

    t2 = PostgresOperator(
        task_id="upsert_agg_table_city_day_summary_temerature",
        sql="city_day_summary_temerature.sql",
        postgres_conn_id="weather_db_postgres",
    )
    t1 >> t2
