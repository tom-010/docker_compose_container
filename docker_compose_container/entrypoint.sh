#!/bin/sh
cd /project/


# use -p only if there is $NAME set
[ ! -z "$NAME"] && $NAME="-p $NAME"

cat ./docker-compose.yml | python3 /adjust_docker_compose.py | docker-compose $NAME -f - up --build

#docker-compose -p project1 up --build