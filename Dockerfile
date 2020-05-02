FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

RUN pip install pipenv
RUN pipenv --python 3.8
ADD Pipfile /code/
RUN pipenv install --dev
