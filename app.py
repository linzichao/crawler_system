import boto3

import os
import json
import re
import ast
import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse

from flask import Flask
from flask import request

load_dotenv()

app = Flask(__name__)

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY')
)

s3_resource = boto3.resource(
    's3', 
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY')
)

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/set_urls', methods=['POST'])
def set_urls():
    data = request.get_json()
    
    if not 'url' in data.keys():
        return 'The format of parameter is incorrect!'

    # record urls in S3
    obj = s3_resource.Object('appier-crawler', 'urls')
    obj.put(Body=str(data).encode('ascii'))
    
    for u in data['url']:
        domain = urlparse(u).netloc
        key = 'domain/' + domain
        objs = list(s3_resource.Bucket('appier-crawler').objects.filter(Prefix=key))
        obj = s3_resource.Object('appier-crawler', key)
        url_collection = []
        
        # check whether the domain has been saved 
        if any([w.key == key for w in objs]):
            url_collection = ast.literal_eval(obj.get()['Body'].read().decode('ascii'))
            if u not in url_collection:
                url_collection.append(u)
        else:
            url_collection = [u]

        obj.put(Body=str(url_collection).encode('ascii'))
    
    return 'status: OK'


@app.route('/retrieve_by_url', methods=['GET'])
def retrieve_by_url():
    if not 'url' in request.args:
        return 'You need the parameter "url" in GET request!'
    url = request.args.get('url')
    
    if url.startswith('http'):
        url = re.sub(r'https?://', '', url)

    key = 'celery/celery-task-meta-' + url
    objs = list(s3_resource.Bucket('appier-crawler').objects.filter(Prefix=key))
    obj = s3_resource.Object('appier-crawler', key)
    
    if any([w.key == key for w in objs]):
        return obj.get()['Body'].read().decode('ascii')
    return 'This url has not been scraped!'


@app.route('/retrieve_by_urls', methods=['POST'])
def retrieve_by_urls():
    data = request.get_json()
    
    if not 'url' in data.keys():
        return 'The format of parameter is incorrect!'
    
    res = {}
    for u in data['url']:
        if u.startswith('http'):
            u = re.sub(r'https?://', '', u)
        key = 'celery/celery-task-meta-' + u
        objs = list(s3_resource.Bucket('appier-crawler').objects.filter(Prefix=key))
        obj = s3_resource.Object('appier-crawler', key)
        
        if any([w.key == key for w in objs]):
            res[u] = obj.get()['Body'].read().decode('ascii')
    return res


@app.route('/retrieve_by_domain')
def retrieve_by_domain():
    if not 'domain' in request.args:
        return 'You need the parameter "domain" in GET request!'
    domain = request.args.get('domain')
    
    key = 'domain/' + domain
    objs = list(s3_resource.Bucket('appier-crawler').objects.filter(Prefix=key))
    obj = s3_resource.Object('appier-crawler', key)
    
    if any([w.key == key for w in objs]):
        
        url_collection = ast.literal_eval(obj.get()['Body'].read().decode('ascii'))
        res = {}
        for u in url_collection:
            if u.startswith('http'):
                u = re.sub(r'https?://', '', u)
            u_key = 'celery/celery-task-meta-' + u
            print(u_key)
            u_objs = list(s3_resource.Bucket('appier-crawler').objects.filter(Prefix=u_key))
            u_obj = s3_resource.Object('appier-crawler', u_key)
            if any([w.key == u_key for w in u_objs]):
                res[u] = u_obj.get()['Body'].read().decode('ascii')
        return res
    
    return 'This domain has not been scraped!'

@app.route('/test')
def test():
    res = []
    scrape_results = s3_client.list_objects_v2(Bucket='appier-crawler', Prefix='celery')['Contents']
    for o in scrape_results:
        if o['Key'] == 'celery/': continue
        
        dt = o['LastModified'].replace(tzinfo=None)
        print(o['Key'] + ' ' + str(o['LastModified']))

        if (datetime.datetime.now() - dt).days < 1:
            s3_client.delete_object(Bucket='appier-crawler', Key=o['Key'])
        

    return 'True'

