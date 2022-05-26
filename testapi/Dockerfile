# syntax=docker/dockerfile:1.2
FROM python:3.10.4-slim AS base

RUN apt-get update -qy && \
    apt-get install -qy \
        curl && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

RUN poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --no-dev

COPY testapi ./testapi


FROM base AS test
COPY tests ./tests
ENTRYPOINT ["poetry", "run", "pytest"]
CMD ["tests/"]


FROM base AS app
CMD exec uvicorn --host 0.0.0.0 --port $PORT --proxy-headers testapi.app:app
