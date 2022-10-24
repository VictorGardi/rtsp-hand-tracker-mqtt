import os

import numpy as np
import streamlit as st

from helpers import byte_array_to_pil_image
from mqtt import connect_to_mqtt_broker

VIEWER_WIDTH = 600


def get_random_numpy():
    """Return a dummy frame."""
    return np.random.randint(0, 100, size=(32, 32))


title = st.title("MQTT viewer")
viewer = st.image(get_random_numpy(), width=VIEWER_WIDTH)
test = st.empty()


def on_message(client, userdata, msg):
    if msg.topic != "home/camera/capture":
        return
    image = byte_array_to_pil_image(msg.payload)
    image = image.convert("RGB")
    viewer.image(image, width=VIEWER_WIDTH)


def main():
    client = connect_to_mqtt_broker(os.environ["MQTT_USER"], os.environ["MQTT_PW"])
    client.on_message = on_message
    client.connect(os.environ["MQTT_BROKER_IP"])
    client.subscribe("home/camera/capture")
    client.loop_forever()


if __name__ == "__main__":
    main()
