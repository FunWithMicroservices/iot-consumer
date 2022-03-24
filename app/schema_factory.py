import requests
import logging

from datetime import datetime

import io
import avro.schema
import avro.io

from settings import SCHEMA_REGISTRY_URL, TOPICS, INFLUX_CLIENT


logger = logging.getLogger(__name__)


__all__ = ("schemas", )


class _Schemas:
    def __init__(self):
        valid_schema_names = [
            schema_name 
            for schema_name in self.get_registered_schema_names()
            if schema_name.replace("-value", "") in TOPICS
        ]
        self._schemas = dict()
        for schema_name in valid_schema_names:
            key = schema_name.replace("-value", "")
            self._schemas[key] = self.get_avro_schema(schema_name)

    @classmethod
    def get_registered_schema_names(cls):
        response = requests.get(
            url=f'{SCHEMA_REGISTRY_URL}/subjects'
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_latest_schema_version(cls, schema_name: str):
        response = requests.get(
            url=f'{SCHEMA_REGISTRY_URL}/subjects/{schema_name}/versions'
        )
        response.raise_for_status()
        return response.json()[-1]

    @classmethod
    def get_avro_schema_dict(cls, schema_name: str):
        version = cls.get_latest_schema_version(schema_name)
        response = requests.get(
            url=f'{SCHEMA_REGISTRY_URL}/subjects/{schema_name}/versions/{version}'
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_avro_schema(cls, schema_name: str):
        avro_schema_dict = cls.get_avro_schema_dict(schema_name)
        return avro.schema.parse(avro_schema_dict['schema'])

    def avro_message_parser(self, message):
        topic = message.topic()
        message_value = message.value()
        bytes_reader = io.BytesIO(message_value)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(self._schemas[topic])
        decoded_msg = reader.read(decoder)
        return decoded_msg

    def write_to_influx(self, message):
        topic = message.topic()
        logger.info(f"Received message from topic {topic}")
        measurement = topic.replace("iot-", "").replace("-data", "")
        decoded_msg = self.avro_message_parser(message)
        logger.info(f"Decoded message: {decoded_msg}")
        time = decoded_msg.pop("timestamp")
        tags = {"car_id": decoded_msg.pop("car_id")}
        
        influx_dict = {
            "measurement": measurement,
            "time": datetime.fromtimestamp(time),
            "tags": tags,
            "fields": decoded_msg
        }
        logger.info(f"Write message into influx measurement {measurement}")
        INFLUX_CLIENT.write_points([influx_dict])

schemas = _Schemas()
