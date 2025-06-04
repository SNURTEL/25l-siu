#!/usr/bin/env bash

set -euo pipefail

docker exec siu bash -c "sed -i 's/frame\.show()/\/\/frame.show()/g' /root/siu_ws/src/ros_tutorials/turtlesim/src/turtlesim.cpp && \
    cd /root/siu_ws && \
    source /opt/ros/noetic/setup.bash && \
    catkin build"