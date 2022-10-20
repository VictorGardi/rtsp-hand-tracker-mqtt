# rtsp-tracker
Tracker that listens to a live rstp stream, does hand tracking and publishes
the number of fingers identified as an mqtt package.

## Get started
1. Build docker image
```bash
docker-compose build
```
2. Add a .env file with the following variables
-   CAMERA_IP: IP address of internet camera
-   CAMERA_USER: Camera username
-   CAMERA_PW: Camera password
-   MQTT_USER: MQTT broker username
-   MQTT_PW: MQTT broker password

3. Start docker container
```bash
docker-compose up
```
4. The default MQTT topic is home/camera/number_of_fingers
