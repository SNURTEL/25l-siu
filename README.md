# SIU

Development environment for SIU project

`code` directory, `roads.png` and `routes.csv` are mounted so they can be edited while the container is running. `models` directory is mounted as well and it is where models are written to

## Stage 2

Setup the environment (run the Docker image and connect to LXDE over VNC)

```shell
./01-run_env.sh
```

Install missing packages (namely: tensorflow xd) and start the turtle environment in the background:

```shell
./02-setup_env.sh
```

Now you can start training models:

```shell
./03-exec_turtle_script.sh code/dqn_single.py
```

To test model and view turtle running constantly:

```shell
./04-run-test.sh code/play_single.py models/model_file.tf
```

When you have a working model, prepare the docker image with all required files included:

```shell
docker build --build-arg MODEL_PATH=models/<MODEL>.tf -t siu-stage2 .
```

Verify the image is working:

```shell
docker run --name siu-stage2 -p 6080:80 siu-stage2
```

Open [localhost:6080](http://localhost:6080) in your web browser and run `bash siu-stage2-demo.sh` in LXDE terminal. The route should open, and after a few seconds the turtle should start running.

## Misc

When you're done, you can delete the container:

```shell
docker rm --force siu
```
