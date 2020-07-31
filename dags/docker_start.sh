#!/bin/bash
python3 ./crawler_dag.py
python3 ./cleanup_dag.py
celery worker -A celery_config --loglevel=info > celery_worker.log 2> celery_worker_err.log &

airflow initdb

cd ..
cp -r dags /root/airflow/
cp .env /root/airflow/dags/
airflow webserver -p 8080 > airflow_web.log 2> airflow_web_err.log &
airflow scheduler > airflow_scheduler.log 2> airflow_scheduler_err.log &

python3 -m flask run --host=0.0.0.0
