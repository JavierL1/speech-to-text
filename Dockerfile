FROM jrottenberg/ffmpeg:4.1-ubuntu

RUN apt update && apt-get install -y make automake gcc g++ subversion python3-pip

WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./app .
WORKDIR /app/src

ENTRYPOINT ["/usr/bin/env"]

CMD ["python3", "run.py"]
