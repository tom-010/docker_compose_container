#!/bin/bash

docker run -it \
    -e PORTS="8081:80" \
    -e NAME="tom" \
    -v /var/run/docker.sock:/var/run/docker.sock \
    playground
