FROM python:3.9
ARG XAUTH_TOKEN
# cv2 dependencies
RUN apt-get update && apt-get install libgl1 -y && \
                      apt-get install net-tools -y && \
                      apt-get install libsm6 && \
                      apt-get install xauth -y && \
                      xauth add ${XAUTH_TOKEN}
WORKDIR /app
#COPY . ./
COPY requirements.txt .

RUN pip install -r requirements.txt
