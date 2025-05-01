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


When you're done, you can delete the container:

```shell
docker rm --force siu
```
