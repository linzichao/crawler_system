FROM python:3.6
ADD . /code
WORKDIR /code
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

WORKDIR /code/dags
RUN chmod +x ./docker_start.sh
CMD ./docker_start.sh

EXPOSE 8080 5000
