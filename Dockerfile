FROM python:3.12-slim

RUN apt update
RUN mkdir -p /assignment

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /assignment
EXPOSE 8000

COPY ./src ./src
COPY ./commands ./commands
COPY ./src/fixtures ./src/fixtures

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

RUN adduser --disabled-password sauberr-user


USER sauberr-user