import boto3

import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

load_dotenv()

s3_client = boto3.client(
    's3', 
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY')
)

args = {
    'owner': 'linzichao',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='cleanup_version_1',
    default_args=args,
    schedule_interval="@daily",
    tags=['test']
)

def cleanup(ds, **kwargs):
    scrape_results = s3_client.list_objects_v2(Bucket='appier-crawler', Prefix='celery')['Contents']
    for o in scrape_results:
        if o['Key'] == 'celery/': continue
        dt = o['LastModified'].replace(tzinfo=None)

        if (datetime.now() - dt).days >= 30:
            print(o['Key'] + ' is deleting!')
            s3_client.delete_object(Bucket='appier-crawler', Key=o['Key'])


task = PythonOperator(
    task_id='test_cleanup',
    provide_context=True,
    python_callable=cleanup,
    dag=dag,
)
