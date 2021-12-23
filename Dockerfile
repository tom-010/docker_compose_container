FROM docker/compose:debian-1.29.2

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install pyyaml

WORKDIR /project

COPY ./entrypoint.sh /
COPY ./adjust_docker_compose.py /

ENTRYPOINT [ "/entrypoint.sh" ]

