FROM python:3.10-slim

WORKDIR /app

COPY wait-for-it.sh /app/

COPY . /app/

RUN apt-get update \
    && apt-get install -y gcc

RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py migrate \
    && python manage.py runserver 0.0.0.0:8000