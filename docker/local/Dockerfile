FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/YlabDishes

RUN apk update && apk upgrade

COPY ./ ./

RUN pip install --upgrade pip && pip install -r requirements.txt
