FROM python:3.6.2 as base

COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt


FROM python:3.6.2
COPY --from=base /root/.cache /root/.cache

COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt && \
    rm -rf /root/.cache

COPY script.py /app/script.py

CMD ["python", "/app/script.py"]
