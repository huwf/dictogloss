FROM python:3.6

RUN  useradd -m worker -u 1000 && apt update && apt install -y ffmpeg
USER worker
WORKDIR /usr/src

COPY --chown=1000:1000 requirements.txt ./requirements.txt

RUN pip install --user -r requirements.txt
