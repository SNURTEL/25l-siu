#!/usr/bin/env bash

set -euo pipefail
set -x
docker exec -i --tty=false siu bash -s <<-EOF 
    source /root/siu_ws/devel/setup.bash && (apt update || true) \\
    && DEBIAN_FRONTEND=noninteractive apt install -y python3-pip \\
    && python3 -m pip install --upgrade pip \\
    && python3 -m pip install tensorflow \\
    && (DISPLAY=:1.0 roslaunch turtlesim siu.launch &)
EOF


