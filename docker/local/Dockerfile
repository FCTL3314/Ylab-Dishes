FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/YlabDishes

COPY ./ ./

RUN pip install --upgrade pip && pip install -r requirements.txt
