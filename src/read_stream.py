import argparse
import logging
import os
import time

from cvzone.HandTrackingModule import HandDetector
from environs import Env
from vidgear.gears import WriteGear

from helpers import get_player_from_ip_camera, get_player_from_webcam
from mqtt import get_mqtt_client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

env = Env()

SINK_STREAM: str = env("SINK_STREAM")
LOG_LEVEL = env.log_level("LOG_LEVEL", logging.WARNING)
VERBOSE = LOG_LEVEL <= logging.INFO


def stream_video(ip: str, frame_rate: int = 2) -> None:
    logger.info("Selecting device...")
    if "localhost" in ip:
        player = get_player_from_webcam()
    else:
        player = get_player_from_ip_camera(ip)

    # logger.info("Loading face detector...")
    # detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    prev: float = 0
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    client = get_mqtt_client(os.environ["MQTT_USER"], os.environ["MQTT_PW"])
    client.connect(os.environ["MQTT_BROKER_IP"])
    sink = WriteGear(
        output_filename=SINK_STREAM,
        logging=VERBOSE,
        **{
            "-f": "rtsp",
            "-rtsp_transport": "tcp",
            "-tune": "zerolatency",
            "-preset": "ultrafast",
            "-stimeout": "1000000",
            "-input_framerate": frame_rate,
            "-r": frame_rate,
        }
    )

    while True:
        time_elapsed = time.time() - prev
        frame = player.read()
        if time_elapsed > 1.0 / frame_rate:
            # img = rescale_frame(img, percent=50)
            prev = time.time()
            # faces = haar_find_faces(frame, detector)
            # if len(faces) > 0:
            #    print(faces)
            #    frame = plot_haar_faces(frame, faces)
            hands, frame = detector.findHands(frame, draw=True)  # with draw

            if hands:
                fingers = list()
                for hand in hands:
                    # lmList1 = hand["lmList"]  # List of 21 Landmark points
                    # bbox1 = hand["bbox"]  # Bounding box info x,y,w,h
                    # centerPoint1 = hand["center"]  # center of the hand cx,cy
                    # handType1 = hand["type"]  # Handtype Left or Right
                    fingers += detector.fingersUp(hand)
                msg = sum(fingers)
            else:
                msg = "unavailable"
            client.publish(os.environ["MQTT_TOPIC"], msg)
            sink.write(frame, rgb_mode=True)
        # player.stop()
        # sink.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="print debug messages to stderr")
    parser.add_argument("--prod", action="store_true", help="Run in production mode")
    args = parser.parse_args()
    DEBUG = args.debug
    stream_video(os.environ["CAMERA_IP"])
