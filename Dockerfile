FROM python:3.10.7-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /w34-backend


# create directory for the app user
# RUN mkdir -p /home/app

# create the app user
# RUN adduser --system --group app

# ENV HOME=/home/app
# ENV APP_HOME=/home/app/web
# RUN mkdir $APP_HOME
# WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y libpq-dev python3-dev gcc

COPY requirements.txt /w34-backend/
RUN pip install -r requirements.txt

COPY . ./

# RUN chown -R app:app $APP_HOME

# USER app
