FROM python:3.9

LABEL author="Youness Id bakkasse <hi@younessidbakkasse>" \
      version="1.0.0"

ENV PYTHONUNBUFFERED=1 

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN apt-get update && pip install -r requirements.txt

RUN adduser user 

USER user 