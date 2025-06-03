$ErrorActionPreference = "Stop"

docker run `
  --name siu `
  -p 6080:80 `
  -e RESOLUTION=1920x1080 `
  --volume "${PWD}/code:/root/code" `
  --volume "${PWD}/roads_multi.png:/roads.png" `
  --volume "${PWD}/routes_multi.csv:/root/routes.csv" `
  --volume "${PWD}/models:/root/models" `
  --detach `
  dudekw/siu-20.04