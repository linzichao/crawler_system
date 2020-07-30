import logging

import requests
import redis
import celery
from celery.utils.log import get_task_logger
from celery_config import app

from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urlparse

LOGGER = get_task_logger(__name__)

@app.task
def fetch(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')
    LOGGER.info('Crawling success at time %s!', time.asctime(time.localtime(time.time())))
    
    data, metadata = {}, {}
    metadata['url'] = url
    metadata['domain'] = urlparse(url).netloc
    metadata['title'] = soup.title.text
    #metadata['meta'] = str(soup.find_all("meta"))

    data['time'] = time.asctime(time.localtime(time.time()))
    data['context'] = response.text
    data['metadata'] = metadata
    return data
