FROM python:3.8-buster

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libopenblas-dev \
    libopencv-dev

RUN pip install Flask pandas joblib flask-cors autogluon

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
