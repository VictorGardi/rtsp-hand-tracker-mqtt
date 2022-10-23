import os
import logging
from paho.mqtt import client

logger = logging.getLogger(__name__)

def connect_to_mqtt_broker(mqtt_broker_ip: str, mqtt_user: str, mqtt_pw: str) -> client.Client:
    mqtt_client = client.Client(
        client_id=mqtt_broker_ip,
        clean_session=True,
        userdata=None,
        protocol=client.MQTTv311,
        transport="tcp",
    )
    mqtt_client.username_pw_set(username=mqtt_user, password=mqtt_pw)
    mqtt_client.connect(mqtt_broker_ip)
    logger.info(f"Successfully connected to {mqtt_broker_ip}")    
    return mqtt_client
