FROM python:3.7.10-slim

RUN python3 -m pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev && \
    rm -r /root/.cache/pypoetry/

COPY . ./

WORKDIR /
ENTRYPOINT ["python3", "/app/main.py"]
