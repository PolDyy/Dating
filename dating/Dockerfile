FROM python:3.10-alpine as builder

WORKDIR /srv/www/dating

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /srv/www/dating/wheels -r requirements.txt


FROM python:3.10-alpine

WORKDIR /srv/www/dating

COPY --from=builder  /srv/www/dating/wheels /wheels
COPY . .

RUN pip install --no-cache /wheels/*

EXPOSE 8000

RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
