FROM python:3.9
ARG XAUTH_TOKEN
# cv2 dependencies
RUN apt update && apt install libgl1 net-tools libsm6 xauth -y
#RUN xauth add ${XAUTH_TOKEN} | echo "DEBUG mode will fail"
#RUN mkdir -p /root/.streamlit && bash -c 'echo -e "\
#                                        [general]\n\
#                                        email = \"your-email@domain.com\"\n\
#                                        " > /root/.streamlit/credentials.toml'

WORKDIR /app
ENV PYTHONPATH="$PYTHONPATH:/app"
COPY requirements.txt .

RUN pip install -r requirements.txt
