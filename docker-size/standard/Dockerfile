FROM python:3.6.9

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf /root/.cache

COPY script.py /app/script.py

CMD ["python", "/app/script.py"]
