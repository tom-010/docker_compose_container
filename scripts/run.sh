#!/bin/bash

# First, bring the parent container up-to-date
cd docker_compose_container
docker build . -t tom010/docker-compose-container:latest
cd ..


cd playground

# fresh start for every build
docker rmi  playground --force
docker build . -t playground -f Dockerfile.bundle || exit 1

echo ""
echo ""
echo "###################################################"
echo "###################################################"
echo "The image was built."
echo "Now we are running it..."
echo "###################################################"
echo "###################################################"
echo ""
echo ""

# we delete the container on this machine and expect that it is 
# still stored in the playground container. The test fails 
# if it downloads it on statup
docker rmi nginxdemos/hello:0.2-plain-text --force > /dev/null

cd ..

./scripts/start.sh