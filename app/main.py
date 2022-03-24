import logging
import sys
from pathlib import Path


from settings import CONSUMER
from schema_factory import schemas

from settings import LOG_DIR

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
log_format = logging.Formatter(
    "%(asctime)s %(levelname)-8s %(name)-8s %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

Path.mkdir(LOG_DIR, exist_ok=True)
file_logger = logging.FileHandler(LOG_DIR / "app.log")
file_logger.setFormatter(log_format)
logger.addHandler(file_logger)


while True:
    logger.info("Start consuming")
    msg = CONSUMER.poll(timeout=1.0)
    if msg is None:
        logger.info("Nothing To Do")
    elif msg.error():
        logger.error(f"{msg.error()}")
    else:
        logger.info("Message received")
        try:
            decoded_msg = schemas.write_to_influx(msg)
        except AssertionError:
            continue
