FROM python:3.12-slim

RUN apt update
RUN mkdir /test_assignment

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /test_assignment
EXPOSE 8000

COPY ./src ./src
COPY ./commands ./commands

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

RUN adduser --disabled-password sauberr-user

USER sauberr-user
