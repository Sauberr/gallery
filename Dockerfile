FROM python:3.12-slim

RUN apt update
RUN mkdir -p /assignment

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /assignment
EXPOSE 8000

COPY ./pyproject.toml ./poetry.lock ./

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
RUN poetry install --no-root --only main --no-interaction --no-ansi

COPY ./src ./src
COPY ./commands ./commands
COPY ./src/fixtures ./src/fixtures


RUN adduser --disabled-password sauberr-user

USER sauberr-user