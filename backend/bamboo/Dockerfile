FROM alpine:3.8

RUN mkdir /app
COPY requirements.txt /app
COPY build-status.py /app

RUN apk update && \
    apk add ca-certificates python3 && \
    rm -rf /var/cache/apk/*


RUN pip3 install -r /app/requirements.txt

ENTRYPOINT [ "/usr/bin/python3", "/app/build-status.py" ]
