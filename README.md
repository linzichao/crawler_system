# Crawler System 
Airflow + Celery + Docker + AWS S3 crawler system

## How to use
The system has been deployed to [http://140.119.19.117:5000/](http://140.119.19.117:5000/) and [http://140.119.19.117:8080/](http://140.119.19.117:8080/). Please refer to [API docs](#api-docs).

## System Architecture
![Imgur](https://i.imgur.com/pUevHFV.png)

## API docs

#### set_urls (set the urls you want to scrape)
* **URL**
 /set_urls
* **Method**
 ```POST```
* **URL Params**
 None
* **Data Params**
 (application/json)
 ```{"url": ["https://www.google.com.tw/", "https://www.youtube.com/"]}```
* **Success Response**
 ```'status: OK'```

#### retrieve_by_url (get the scraping result by a single url)
* **URL**
 /retrieve_by_url
* **Method**
 ```GET```
* **URL Params**
 ```url```
* **Data Params**
 None
* **Success Response**
 ```{"status: "SUCCESS", "result": {"time": "Fri Jul 31 11:30:07 2020", "context": "html context...", "metadata": {"url": "https://www.google.com.tw/", "domain": "www.google.com.tw", "title": "Google"}}, "traceback": null, "children": [], "date_done": "2020-07-31T11:30:07.159309", "task_id": "www.google.com.tw/"}}```
* **Example**
 [http://140.119.19.117:5000/retrieve_by_url?url=https://www.google.com.tw/](http://140.119.19.117:5000/retrieve_by_url?url=https://www.google.com.tw/)

#### retrieve_by_urls (get the scraping result by multiple urls)
* **URL**
 /retrieve_by_urls
* **Method**
 ```POST```
* **URL Params**
 None
* **Data Params**
 (application/json)
 ```{"url": ["https://www.google.com.tw/", "https://www.youtube.com/"]}```
* **Success Response**
 ```{"www.google.com.tw/": {retrieve_by_url result}, "www.youtube.com/": {retrieve_by_url result}}```

#### retrieve_by_domain (get the scraping result by a single domain)
* **URL**
 /retrieve_by_domain
* **Method**
 ```GET```
* **URL Params**
 ```domain```
* **Data Params**
 None
* **Success Response**
 ```{"www.google.com.tw/": {retrieve_by_domain result}```
* **Example**
 [http://140.119.19.117:5000/retrieve_by_domain?domain=www.google.com.tw](http://140.119.19.117:5000/retrieve_by_domain?domain=www.google.com.tw)

## Set up at your local
1. Rename the file of environment variables
```
$ mv .env.default .env
```

2. Add your own aws access_key_id and secret_access_key in ```.env``` (create the bucket and directory in S3 if necessary)
```
BROKER=redis://redis:6379
RESULT_BACKEND=s3://appier-crawler
S3_ACCESS_KEY_ID=Your aws access key id
S3_SECRET_ACCESS_KEY=Your aws secret access key 
S3_BUCKET=appier-crawler
S3_BASE_PATH=celery/
```

3. Build docker image and run
```
$ docker-compose up
```

4. Access the airflow panel in [http://localhost:8080/](http://localhost:8080/) and API interface in [http://localhost:5000/](http://localhost:5000/)