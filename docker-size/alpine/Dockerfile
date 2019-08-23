FROM python:3.6.9-alpine

RUN apk add --no-cache build-base gcc && \
    rm -rf /var/cache/apk/*

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf /root/.cache

COPY script.py /app/script.py

CMD ["python", "/app/script.py"]
