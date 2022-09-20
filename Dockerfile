FROM python:3.10.7-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /w34
COPY requirements.txt /w34/

RUN apt-get update && apt-get install -y libpq-dev python3-dev gcc

RUN pip install -r requirements.txt

COPY . /w34/