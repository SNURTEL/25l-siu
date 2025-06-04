#!/usr/bin/env bash

set -euo pipefail

docker run \
  --name siu \
  -p 6080:80 \
  -e RESOLUTION=1920x1080 \
  --volume $(pwd)/code:/root/code \
  --volume $(pwd)/roads_multi.png:/roads.png \
  --volume $(pwd)/routes_multi.csv:/root/routes.csv \
  --volume $(pwd)/models:/root/models \
  --detach \
  dudekw/siu-20.04

sleep 5
firefox \
  --width 1920 \
  --height 1080 \
  --url http://localhost:6080
