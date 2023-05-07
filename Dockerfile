FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt
RUN pip install mysqlclient

COPY . .

ENV FLASK_APP=main.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
