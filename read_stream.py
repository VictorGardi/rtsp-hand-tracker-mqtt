import os
import struct
import socket
import time
import logging
from io import BytesIO
from typing import Tuple
import numpy as np
import cv2
from cv2 import VideoCapture

#from object_detection import model, detect_objects
#from retinaface import RetinaFace

logger = logging.getLogger(__file__)



""" TODO: 
        - find faces in img
        - Do facerecognition on faces
        - Create webpage where stream can be seen
        - Save data for x hours. But maybe only data where faces exist? also save faces found and link to time in video
        - Create python lib
        - Run on server. Docker?
""" 

def get_player_from_ip_camera(rtsp_url: str) -> VideoCapture:
    """ Generate player

    Args:
        rtsp_url (str): rtsp_url as "rtsp://user:pw@camera_ip"

    Returns:
        VideoCapture: opencv player
    """
    return cv2.VideoCapture(rtsp_url)

def get_player_from_webcam():
    return cv2.VideoCapture(0)

def generate_rtsp_url(ip: str, hq: bool=True) -> str:
    """ Generate correct ip format, i.e. "rtsp://user:pw@ip".
        Environment variables CAMERA_USER and CAMERA_PW is needed.

    Args:
        ip (str): camera ip

    Returns:
        str: rtsp_url as "rtsp://user:pw@camera_ip"
    """
    user = os.environ["CAMERA_USER"]
    pw = os.environ["CAMERA_PW"]
    if hq:
        stream = "stream1"
    else:
        stream = "stream2"
    return f"rtsp://{user}:{pw}@{ip}/{stream}"

def stream_video(ip: str, frame_rate: int = 2) -> None:
    rtsp_url = generate_rtsp_url(ip)
    player = get_player_from_ip_camera(rtsp_url)
    #player = get_player_from_webcam()

    logger.info("loading face detector...")
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    prev = 0
    connected = False
    while player.isOpened():
        if not connected:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('localhost', 8080))
                connected = True
                logger.info("Connected")
            except ConnectionRefusedError:
                connected = False
        time_elapsed = time.time() - prev
        _, frame = player.read()
        if time_elapsed > 1./frame_rate:
            frame = rescale_frame(frame, percent=50)
            prev = time.time()
            #faces = RetinaFace.detect_faces(frame)
            #frame = plot_faces(frame, faces)
            faces = haar_find_faces(frame, detector)
            if len(faces) > 0:
                print(faces)
                frame = plot_haar_faces(frame, faces)
            # results = detect_objects(frame, model)
            # frame = plot_boxes(results, frame, model)

            #if people_present(results):
            #    find_faces(results, frame, detector)
                #frame = plot_boxes(results, frame, model)


            # try:
            #     cv2.imshow("Wyze v2 camera", frame)
            # except cv2.error as e:
            #     logger.warning(e)

            # # Quit when 'x' is pressed
            # if cv2.waitKey(1) & 0xFF == ord('x'):
            #     break
            if connected:
                memfile = BytesIO()
                np.save(memfile, frame)
                memfile.seek(0)
                data = memfile.read()
                try:
                   # Send form byte array: frame size + frame content
                   client_socket.sendall(struct.pack("L", len(data)) + data)
                except OSError:
                    connected = False

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    player.release()

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def plot_haar_faces(frame, faces):
    for (x, y, w, h) in faces:
        # draw the face bounding box on the image
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame

def people_present(results: Tuple) -> bool:
    labels, cord = results
    if 0 not in labels:
       logger.info("No humans found")
       return False
    else:
        return True

def haar_find_faces(frame, detector) -> np.ndarray:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # perform face detection
    return detector.detectMultiScale(gray, scaleFactor=1.25,
                                      minNeighbors=5, minSize=(64, 64),
                                      flags=cv2.CASCADE_SCALE_IMAGE)

def find_faces(results: Tuple, frame, detector):
    labels, coord = results
    people_indices = [i for i, x in enumerate(labels) if x == 0]
    for idx in people_indices:
        row = coord[idx]
        # If score is less than 0.2 we avoid making a prediction.
        if row[4] < 0.2: 
            continue
        frame = find_face(frame, detector)


def plot_boxes(results, frame, model):
    labels, cord = results
    if 0 not in labels:
       logger.info("No humans found")
       return frame
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]
    for i in range(n):
        row = cord[i]
        # If score is less than 0.2 we avoid making a prediction.
        if row[4] < 0.2: 
            continue
        x1 = int(row[0]*x_shape)
        y1 = int(row[1]*y_shape)
        x2 = int(row[2]*x_shape)
        y2 = int(row[3]*y_shape)
        bgr = (0, 255, 0) # color of the box
        label_font = cv2.FONT_HERSHEY_SIMPLEX #Font for the label.
        cv2.rectangle(frame, \
                      (x1, y1), (x2, y2), \
                       bgr, 2) #Plot the boxes
        confidence = str(round(row[4], 3))
        cv2.putText(frame,\
                    model.names[labels[i]] + f" {confidence}", \
                    (x1, y1), \
                    label_font, 0.9, bgr, 2) #Put a label over box.
        return frame

if __name__ == "__main__":
    if "CAMERA_USER" not in os.environ:
        raise ValueError("CAMERA_USER needs to be set as env variables!")
    elif "CAMERA_PW" not in os.environ:
        raise ValueError("CAMERA_PW needs to be set as env variables!")

    ip = "192.168.0.128"
    stream_video(ip)
    
    

