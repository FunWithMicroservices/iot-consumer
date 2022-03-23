FROM python:3.8-slim-buster

RUN apt-get update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# WAITER
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# Python App
COPY ./app /app/

RUN pip install --upgrade pip \
    && pip install -r app/requirements.txt

WORKDIR /app/
CMD ["python", "main.py"]
