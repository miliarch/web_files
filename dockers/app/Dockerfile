FROM python:3.9-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./
ARG FLASK_APP=app FLASK_ENV=development
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
