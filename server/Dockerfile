FROM python:3.6

RUN useradd -m worker -u 1000 && chown -R worker:worker /usr/src && apt update && apt install -y ffmpeg

USER worker
WORKDIR /usr/src

COPY --chown=1000:1000 requirements.txt ./requirements.txt

RUN pip install --user -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="API_KEY.json"
ENV FLASK_APP="server.api.api"
ENV FLASK_RUN_HOST="0.0.0.0"

COPY --chown=1000:1000 ./ ./server


CMD python -u -m flask run