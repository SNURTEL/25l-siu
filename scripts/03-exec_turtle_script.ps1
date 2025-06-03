# $args[0] is the script name passed to this script

$ErrorActionPreference = "Stop"

$scriptName = $args[0]

$command = @"
source /root/siu_ws/devel/setup.bash && PYTHONPATH=`$PYTHONPATH:/root/code python3 "/root/$scriptName"
"@

docker exec siu bash -c "$command"