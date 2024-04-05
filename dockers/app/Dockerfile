FROM python:3.9-alpine

ARG USER_NAME=flask
ARG USER_ID=1000
RUN adduser -D -H -u $USER_ID $USER_NAME

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER $USER_NAME
COPY app ./
ARG FLASK_APP=app FLASK_ENV=development
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
