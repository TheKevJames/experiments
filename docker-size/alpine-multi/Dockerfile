FROM python:3.6.2-alpine as base

RUN apk add --no-cache build-base gcc && \
    rm -rf /var/cache/apk/*

COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt


FROM python:3.6.2-alpine
COPY --from=base /root/.cache /root/.cache

COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt && \
    rm -rf /root/.cache

COPY script.py /app/script.py

CMD ["python", "/app/script.py"]
