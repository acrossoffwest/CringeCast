FROM python:3.12.0a6-alpine3.16

WORKDIR /python-docker

RUN apk add --no-cache pulseaudio alsa-utils alsa-plugins-pulse mpg123

ENV PULSE_SERVER=host.docker.internal

COPY ../requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ../ .

EXPOSE 42069

CMD [ "flask", "--app=CringeCast", "run", "--host=0.0.0.0", "--port=42069"]