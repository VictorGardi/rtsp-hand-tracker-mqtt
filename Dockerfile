FROM python:3.9
# cv2 dependencies
RUN apt update && apt install libgl1 net-tools libsm6 ffmpeg -y

WORKDIR /app
ENV PYTHONPATH="$PYTHONPATH:/app"
COPY requirements.txt .

RUN pip install -r requirements.txt
