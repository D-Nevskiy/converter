FROM python:3.11-slim
RUN mkdir /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . /app
WORKDIR /app

RUN python3 manage.py makemigrations currency &&  \
    python3 manage.py migrate &&  \
    python3 manage.py loaddata data.json

ENTRYPOINT python3 manage.py runserver 0:8000
