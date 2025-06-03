$ErrorActionPreference = "Stop"

docker run `
  --name siu `
  -p 6080:80 `
  -e RESOLUTION=1920x1080 `
  --volume "${PWD}/code:/root/code" `
  --volume "${PWD}/roads.png:/roads.png" `
  --volume "${PWD}/routes.csv:/root/routes.csv" `
  --volume "${PWD}/models:/root/models" `
  --detach `
  dudekw/siu-20.04