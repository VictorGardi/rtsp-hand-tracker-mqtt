import os

from paho.mqtt import client


def connect_to_mqtt_broker() -> client.Client:
    mqtt_client = client.Client(
        client_id=os.environ["MQTT_BROKER_IP"],
        clean_session=True,
        userdata=None,
        protocol=client.MQTTv311,
        transport="tcp",
    )
    mqtt_client.username_pw_set(username=os.environ["MQTT_USER"], password=os.environ["MQTT_PW"])
    mqtt_client.connect(os.environ["MQTT_BROKER_IP"])
    return mqtt_client
