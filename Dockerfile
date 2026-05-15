FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /simple_n8n

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /simple_n8n/


 