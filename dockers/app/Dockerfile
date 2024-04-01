FROM python:3.9-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY web_files ./
ARG FLASK_APP=web_files FLASK_ENV=development
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
