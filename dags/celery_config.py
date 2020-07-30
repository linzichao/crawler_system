from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

class CeleryConfig:
    broker_url = os.getenv('BROKER')
    result_backend = os.getenv('RESULT_BACKEND')
    s3_access_key_id = os.getenv('S3_ACCESS_KEY_ID')
    s3_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
    s3_bucket = os.getenv('S3_BUCKET')
    s3_base_path = os.getenv('S3_BASE_PATH')
    imports = ['tasks']

app = Celery('crawler', config_source=CeleryConfig)

if __name__ == '__main__':
    app.start()

