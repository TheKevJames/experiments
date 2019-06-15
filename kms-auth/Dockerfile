# See https://cloud.google.com/run/docs/quickstarts/build-and-deploy#containerizing
FROM python:3.7.3

RUN pip install "gcloud-aio-kms==2.1.0" "sanic==19.3.1"

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

CMD python /app/server.py
