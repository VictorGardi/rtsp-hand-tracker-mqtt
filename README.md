# rtsp-tracker
Tracker that listens to a live rstp stream, does hand tracking and publishes
the number of fingers identified as an mqtt package.

## Get started
There are two different docker-compose.yml files. docker-compose.qa.yml should be used
for development and this enables use of the webcam (set CAMERA_IP=localhost) of the
host and uses cv2.imshow to display the video in real time.
OBS! If you have chosen localhost as your CAMERA_IP and want to run in DEBUG mode to
see the video, you'll need to run
```
. ./set_xauth_docker_token.sh
```
first. The bash script will find your xauth token and set that to an env variable named
XAUTH_DOCKER_TOKEN. Then you need to run the following to allow the docker container
to use the display of the host.

1. Add a .env in the same directory as the docker-compose files file with the following variables
-   CAMERA_IP: IP address of internet camera (localhost will choose device /dev/video0)
-   CAMERA_USER: Camera username
-   CAMERA_PW: Camera password
-   MQTT_USER: MQTT broker username
-   MQTT_PW: MQTT broker password
-   MQTT_TOPIC: MQTT topic for the message

2. Build docker image
```bash
docker-compose build
```

3. Start docker container in production mode
```bash
docker-compose up
```
3. Start docker container in qa mode
```bash
docker-compose -f docker-compose.qa.yml up
```
