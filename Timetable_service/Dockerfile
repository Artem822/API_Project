FROM python:3.11

WORKDIR /app

ADD . /app/

RUN pip install -r requirements.txt

CMD sleep 21 && python manage.py makemigrations && python manage.py runserver 0.0.0.0:8000

EXPOSE 8000