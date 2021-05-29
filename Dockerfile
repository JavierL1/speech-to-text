FROM jrottenberg/ffmpeg:4.1-alpine

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev jpeg-dev zlib-dev
RUN python3 -m ensurepip

WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./app .
WORKDIR /app/src

ENTRYPOINT ["/usr/bin/env"]

CMD ["python3", "run.py"]
