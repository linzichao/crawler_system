import boto3

import os
from dotenv import load_dotenv
import time
import ast
import re
from urllib.parse import urlparse
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import tasks

load_dotenv()

s3_resource = boto3.resource(
    's3', 
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY')
)

args = {
    'owner': 'linzichao',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='scraping_version_1',
    default_args=args,
    schedule_interval=None,
    tags=['test']
)

def crawler(ds, **kwargs):
    obj = s3_resource.Object('appier-crawler', 'urls')
    urls = ast.literal_eval(obj.get()['Body'].read().decode('ascii'))
    for u in urls['url']:
        _id = u
        if _id.startswith('http'):
            _id = re.sub(r'https?://', '', _id)
        result = tasks.fetch.apply_async([u], task_id=_id)
        print('url: ' + u + ' is scraping!')


task = PythonOperator(
    task_id='test_crawler',
    provide_context=True,
    python_callable=crawler,
    dag=dag,
)
