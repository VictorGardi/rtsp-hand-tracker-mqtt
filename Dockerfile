FROM python:3.9

# cv2 dependencies
RUN apt-get update && apt-get install libgl1 -y && apt-get install net-tools -y

WORKDIR /app
#COPY . ./
COPY requirements.txt .

RUN pip install -r requirements.txt
