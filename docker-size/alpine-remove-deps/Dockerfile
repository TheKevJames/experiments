FROM python:3.6.9-alpine

COPY requirements.txt /app/requirements.txt
RUN apk add --no-cache build-base gcc && \
    python -m pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf /root/.cache && \
    apk del build-base gcc && \
    rm -rf /var/cache/apk/*

COPY script.py /app/script.py

CMD ["python", "/app/script.py"]
