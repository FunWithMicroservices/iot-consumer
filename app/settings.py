import os
from pathlib import Path
from confluent_kafka import Consumer
from influxdb import InfluxDBClient

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve(strict=True).parent
SCHEMA_REGISTRY_URL = os.environ["SCHEMA_REGISTRY_URL"]
KAFKA_HOST = os.environ["KAFKA_HOST"]
TOPICS = os.environ["TOPICS"].split()


from uuid import uuid4

kafka_conf = {
    'bootstrap.servers': KAFKA_HOST,
    'group.id': uuid4().hex,
    'session.timeout.ms': 6000,
    'auto.offset.reset': 'earliest'
}


CONSUMER = Consumer(kafka_conf)
CONSUMER.subscribe(TOPICS)

influx_kwargs = {
    "host": os.environ["INFLUX_HOST"],
    "port": int(os.environ["INFLUX_PORT"]),
    "username": os.environ["INFLUX_USERNAME"],
    "password": os.environ["INFLUX_PASSWORD"],
}

INFLUX_CLIENT = InfluxDBClient(**influx_kwargs)
INFLUX_CLIENT.create_database("iot")
INFLUX_CLIENT.switch_database('iot')
