import logging
import os

import cv2
import numpy as np
from cv2 import VideoCapture
from vidgear.gears import CamGear, VideoGear

from read_stream import VERBOSE

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_player_from_ip_camera(ip: str) -> VideoCapture:
    """Generate player

    Args:
        rtsp_url (str): rtsp_url as "rtsp://user:pw@camera_ip"

    Returns:
        VideoCapture: opencv player
    """
    rtsp_url = generate_rtsp_url(ip)
    return CamGear(
        source=rtsp_url,
        colorspace="COLOR_BGR2RGB",
        logging=VERBOSE,
        **{"THREADED_QUEUE_MODE": False, "-fflags": "nobuffer"},
    ).start()
    # return cv2.VideoCapture(rtsp_url)


def get_player_from_webcam():
    logger.info("Connecting to webcam...")
    options = {
        "CAP_PROP_FRAME_WIDTH": 320,  # resolution 320x240
        "CAP_PROP_FRAME_HEIGHT": 240,
        "CAP_PROP_FPS": 60,  # framerate 60fps
    }
    return VideoGear(source=0, logging=True, **options).start()
    # return cv2.VideoCapture(0)


def generate_rtsp_url(ip: str, hq: bool = False) -> str:
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
    logger.info(f"Connecting to rtsp stream on ip: {ip}")
    user = os.environ["CAMERA_USER"]
    pw = os.environ["CAMERA_PW"]
    if hq:
        stream = "stream1"
    else:
        stream = "stream2"
    return f"rtsp://{user}:{pw}@{ip}/{stream}"


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