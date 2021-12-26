#!/bin/sh
cd /project/

cat ./docker-compose.yml | python3 /adjust_docker_compose.py | docker-compose -f - up --build

#docker-compose -p project1 up --build