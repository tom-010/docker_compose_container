#!/bin/bash


cd playground

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

docker rmi nginxdemos/hello:0.2-plain-text --force > /dev/null

cd ..

./scripts/start.sh