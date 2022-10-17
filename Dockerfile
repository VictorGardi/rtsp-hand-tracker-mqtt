FROM python:3.9

WORKDIR /app
COPY . ./

RUN pip install -r requirements.txt
EXPOSE 5000 
EXPOSE 8080
