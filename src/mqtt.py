import logging

from paho.mqtt import client

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Successfully connected to mqtt_broker_ip")
        client.connected_flag = True  # set flag
    else:
        print("Bad connection to MQTT broker, returned code=", rc)


def get_mqtt_client(mqtt_user: str, mqtt_pw: str) -> client.Client:
    mqtt_client = client.Client()
    mqtt_client.username_pw_set(username=mqtt_user, password=mqtt_pw)
    mqtt_client.on_connect = on_connect
    client.connected_flag = False
    return mqtt_client
