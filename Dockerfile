FROM python:3.6

RUN  useradd -m worker -u 1000 && apt update && apt install -y ffmpeg
USER worker
WORKDIR /opt/project

COPY --chown=1000:1000 requirements.txt ./requirements.txt

RUN pip install --user -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="API_KEY.json"
ENV FLASK_APP="app"

COPY --chown=1000:1000 ./ ./

CMD python -u -m flask run