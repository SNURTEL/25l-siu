#!/usr/bin/env bash

set -euo pipefail

docker exec siu bash -c "source /root/siu_ws/devel/setup.bash && \
    (DISPLAY=:1.0 roslaunch turtlesim siu.launch &)"