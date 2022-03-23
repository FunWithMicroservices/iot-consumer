from settings import CONSUMER
from schema_factory import schemas


while True:
    msg = CONSUMER.poll(timeout=1.0)
    if msg is None:
        print("No message received")
    elif msg.error():
        print("An Error occurred")
    else:
        print("Message received: ", msg.value())
        try:
            decoded_msg = schemas.write_to_influx(msg)
        except AssertionError:
            continue
