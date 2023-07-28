FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/YlabDishes

RUN apt -y update && apt -y upgrade

COPY ./ ./

RUN pip install --upgrade pip && pip install -r requirements.txt
