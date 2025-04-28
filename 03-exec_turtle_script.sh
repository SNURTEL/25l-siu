#!/usr/bin/env bash

# $1 - script to run relative to project dir

set -euo pipefail

docker exec siu bash -c "source /root/siu_ws/devel/setup.bash && PYTHONPATH=\$PYTHONPATH:/root/code python3 \"/root/$1\""
