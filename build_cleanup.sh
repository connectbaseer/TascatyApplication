#!/bin/bash
image_count=$(docker images -a -q | wc -l)
if [ $image_count -ge 1 ]
then
docker rmi $(docker images -a -q)
fi
