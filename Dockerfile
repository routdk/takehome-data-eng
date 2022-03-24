# https://stackoverflow.com/questions/67887138/how-to-install-packages-in-airflow-docker-compose
FROM apache/airflow:2.2.3-python3.8
COPY requirements.txt .
RUN pip install -r requirements.txt
# ENV PYTHONPATH "${PYTHONPATH}:${AIRFLOW_HOME}"

