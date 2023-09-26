# syntax=docker/dockerfile:1

FROM ubuntu:latest

WORKDIR /flask-scraper-app

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

COPY . .

RUN apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt update
RUN apt install -f ./google-chrome-stable_current_amd64.deb -y


CMD [ "flask", "--app", "scraper", "run", "--debug", "--host=0.0.0.0"]


# ENTRYPOINT ["tail", "-f", "/dev/null"]