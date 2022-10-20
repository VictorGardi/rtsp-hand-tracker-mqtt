import argparse
import logging
import os
import time

import cv2
import numpy as np
from cv2 import VideoCapture
from cvzone.HandTrackingModule import HandDetector

from mqtt import connect_to_mqtt_broker

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_player_from_ip_camera(rtsp_url: str) -> VideoCapture:
    """Generate player

    Args:
        rtsp_url (str): rtsp_url as "rtsp://user:pw@camera_ip"

    Returns:
        VideoCapture: opencv player
    """
    return cv2.VideoCapture(rtsp_url)


def get_player_from_webcam():
    return cv2.VideoCapture(0)


def generate_rtsp_url(ip: str, hq: bool = True) -> str:
    """Generate correct ip format, i.e. "rtsp://user:pw@ip".
        Environment variables CAMERA_USER and CAMERA_PW is needed.

    Args:
        ip (str): camera ip

    Returns:
        str: rtsp_url as "rtsp://user:pw@camera_ip"
    """
    if "CAMERA_USER" not in os.environ:
        raise ValueError("CAMERA_USER needs to be set as env variables!")
    elif "CAMERA_PW" not in os.environ:
        raise ValueError("CAMERA_PW needs to be set as env variables!")
    user = os.environ["CAMERA_USER"]
    pw = os.environ["CAMERA_PW"]
    if hq:
        stream = "stream1"
    else:
        stream = "stream2"
    return f"rtsp://{user}:{pw}@{ip}/{stream}"


def stream_video(ip: str, frame_rate: int = 2) -> None:
    if not DEBUG:
        rtsp_url = generate_rtsp_url(ip)
        player = get_player_from_ip_camera(rtsp_url)
    else:
        player = get_player_from_webcam()

    logger.info("loading face detector...")
    # detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    prev: float = 0
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    if not DEBUG:
        client = connect_to_mqtt_broker()

    while player.isOpened():
        time_elapsed = time.time() - prev
        _, img = player.read()
        if time_elapsed > 1.0 / frame_rate:
            img = rescale_frame(img, percent=50)
            prev = time.time()
            # faces = haar_find_faces(frame, detector)
            # if len(faces) > 0:
            #    print(faces)
            #    frame = plot_haar_faces(frame, faces)
            hands, img = detector.findHands(img)  # with draw
            if hands:
                # Hand 1
                hand = hands[0]
                # lmList1 = hand["lmList"]  # List of 21 Landmark points
                # bbox1 = hand["bbox"]  # Bounding box info x,y,w,h
                # centerPoint1 = hand["center"]  # center of the hand cx,cy
                # handType1 = hand["type"]  # Handtype Left or Right

                fingers = detector.fingersUp(hand)
                logger.info(f"Number of fingers: {sum(fingers)}")
                logger.info(fingers)
                msg = sum(fingers)
            else:
                msg = "unavailable"
            if not DEBUG:
                client.publish("home/camera/number_of_fingers", msg)

            if DEBUG:
                try:
                    cv2.imshow("Wyze v2 camera", img)
                except cv2.error as e:
                    logger.warning(e)

                # Quit when 'x' is pressed
                if cv2.waitKey(1) & 0xFF == ord("x"):
                    break
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    player.release()


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def plot_haar_faces(frame, faces):
    for (x, y, w, h) in faces:
        # draw the face bounding box on the image
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame


def haar_find_faces(frame, detector) -> np.ndarray:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # perform face detection
    return detector.detectMultiScale(
        gray, scaleFactor=1.25, minNeighbors=5, minSize=(64, 64), flags=cv2.CASCADE_SCALE_IMAGE
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="print debug messages to stderr")
    args = parser.parse_args()
    DEBUG = args.debug

    stream_video(os.environ["CAMERA_IP"])
