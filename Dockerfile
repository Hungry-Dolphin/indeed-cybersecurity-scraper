# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /flask-scraper-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "flask", "--app", "scraper", "run", "--debug", "--host=0.0.0.0"]