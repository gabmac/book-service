# Build stage
FROM python:3.11-slim as build

WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy your application code and install dependencies
COPY poetry.lock pyproject.toml ./


# Install only main dependencies
RUN poetry install --only main
COPY src src

FROM build AS build-test
COPY alembic.ini alembic.ini
COPY alembic alembic

COPY tests tests
RUN poetry install --only dev

# Final stage
FROM gcr.io/distroless/python3-debian12:latest AS api

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/lib/python3.11
COPY --from=build /code /code
WORKDIR /code
ENTRYPOINT ["/usr/bin/python", "-m", "src.api"]

# Final stage
FROM gcr.io/distroless/python3-debian12:latest AS consumer

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/lib/python3.11
COPY --from=build /code /code
WORKDIR /code
ENTRYPOINT ["/usr/bin/python", "-m", "src.consumer"]

FROM build-test AS test
ENTRYPOINT [ "sh", "-c" ]
CMD ["coverage run -m unittest discover -v -s ./tests -p '*test*.py';coverage report;exit 0"]

FROM build as debug-api
ENV PYDEVD_DISABLE_FILE_VALIDATION=1
RUN poetry install --only debugpy
ENTRYPOINT ["sh", "-c", "python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m src.api"]

FROM build as debug-consumer
ENV PYDEVD_DISABLE_FILE_VALIDATION=1
RUN poetry install --only debugpy
ENTRYPOINT ["sh", "-c", "python -m debugpy --wait-for-client --listen 0.0.0.0:5679 -m src.consumer"]
