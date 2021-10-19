#!/bin/bash
image_count=$(docker images -a -q -f dangling=true | wc -l)
if [ $image_count -ge 1 ]
then
docker stop $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -a -q -f dangling=true)
fi
