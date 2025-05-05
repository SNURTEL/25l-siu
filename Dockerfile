FROM dudekw/siu-20.04

ENV RESOLUTION=1920x1080

ARG MODEL_PATH

ADD code /root/code
ADD roads.png /roads.png
ADD routes.csv /root/routes.csv
ADD ${MODEL_PATH} /root/${MODEL_PATH}

RUN cat <<EOF > /root/siu-stage2-demo.sh
#!/usr/bin/env bash
set -euo pipefail
source /root/siu_ws/devel/setup.bash
apt update || true
DEBIAN_FRONTEND=noninteractive apt install -y python3-pip 
python3 -m pip install --upgrade pip
python3 -m pip install tensorflow
DISPLAY=:1.0 roslaunch turtlesim siu.launch &
sleep 5
PYTHONPATH=\$PYTHONPATH:/root/code python3 "/root/code/play_single.py" -m ${MODEL_PATH}
EOF

LABEL siu-stage="2"
