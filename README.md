# rtsp-tracker
Tracker that listens to a live rstp stream, does hand tracking and publishes
the number of fingers identified as an mqtt package.

## Get started
1. Add a .env file with the following variables
-   CAMERA_IP: IP address of internet camera (localhost will choose device /dev/video0)
-   CAMERA_USER: Camera username
-   CAMERA_PW: Camera password
-   MQTT_USER: MQTT broker username
-   MQTT_PW: MQTT broker password

2. Build docker image
```bash
docker-compose build
```
OBS! If you have chosen localhost as your CAMERA_IP and want to run in DEBUG mode to
see the video, you'll need to run 
```
. ./set_xauth_docker_token.sh
```
first. The bash script will find your xauth token and set that to an env variable named
XAUTH_DOCKER_TOKEN. Then you need to run the following to allow the docker container 
to use the display of the host.
```
docker-compose build --build-arg XAUTH_TOKEN=${XAUTH_DOCKER_TOKEN}
```

3. Start docker container
```bash
docker-compose up
```
4. The default MQTT topic is home/camera/number_of_fingers
