# Fun with ROS 2

Robotics is fun and ROS 2 is a must.

In this workshop, we will play around with ROS 2 and Simulating some robots

## Codespaces - branch `tsr`

The `tsr` branch contains a lighter GitHub Codespaces setup for ROS 2 Humble.
It uses VS Code Web as the code editor and exposes a lightweight noVNC desktop
on port `6080` for graphical ROS tools.

The image is based on `ros:humble-ros-base-jammy` and includes:

- ROS 2 Humble development tools, `colcon`, `rosdep` and `vcstool`,
- `turtlesim`,
- RViz 2,
- rqt and common rqt plugins,
- Gazebo Classic integration with TurtleBot3 Gazebo packages,
- a lightweight `Xvfb` + `fluxbox` + `x11vnc` + noVNC desktop.

It intentionally does not install Jupyter, Chromium, gedit, the TurtleBot3
desktop metapackage, Nav2, Cartographer, PlotJuggler, Create3,
Ignition/Fortress or RMF.

### Running in GitHub Codespaces

Use the `tsr` branch when creating the codespace. GitHub Codespaces reads
`.devcontainer/devcontainer.json`, builds `.devcontainer/Dockerfile`, and starts
the lightweight noVNC desktop automatically. Do not run `docker compose` inside
Codespaces for this setup.

1. Push the `tsr` branch to GitHub.
2. Open the repository on GitHub.
3. Select branch `tsr`.
4. Choose `Code` -> `Codespaces` -> `Create codespace on tsr`.
5. Wait until VS Code Web finishes building the devcontainer.
6. Open the `Ports` tab and open forwarded port `6080`.

The port `6080` opens the graphical desktop for ROS GUI applications. If the
browser does not open it automatically, use the forwarded port URL shown by
Codespaces in the `Ports` tab. The noVNC page should open the VNC client
directly and show an `xterm` terminal inside the lightweight desktop.

Run ROS commands in the VS Code Web terminal:

```bash
echo "$ROS_DISTRO"
ros2 --help
```

Run GUI applications from the same terminal and view them through noVNC on port
`6080`:

```bash
ros2 run turtlesim turtlesim_node
rqt_graph
rviz2
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

To edit the system-wide Bash startup file from the noVNC terminal:

```bash
edit-system-bashrc
```

This opens `/etc/bash.bashrc` with `sudo nano`. To edit the user Bash startup
file instead, use:

```bash
nano ~/.bashrc
```

To build the Codespaces image locally:

```bash
docker build -f .devcontainer/Dockerfile -t ros-fun-tsr-humble .
```

The `ros-fun-tsr-humble:latest` image name is a local tag created by the build.
It is not downloaded from DockerHub or GHCR. GitHub Codespaces also builds this
environment directly from `.devcontainer/Dockerfile`.

To run the same lightweight image locally with noVNC:

```bash
docker compose up --build
```

Open [http://localhost:6080](http://localhost:6080) to access the graphical
desktop.

On a Linux host with X11, you can also use the host display instead of noVNC:

```bash
docker compose -f docker-compose-x11.yml up --build
```

Then open a second terminal and enter the running container:

```bash
docker compose -f docker-compose-x11.yml exec ros2 bash
```

Useful checks inside the container:

```bash
echo "$ROS_DISTRO"
ros2 --help
ros2 pkg create --build-type ament_python demo_pkg
colcon build
```

Open forwarded port `6080` to use the graphical desktop. Example GUI commands:

```bash
ros2 run turtlesim turtlesim_node
rqt_graph
rviz2
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

The legacy full laboratory image can still be built from `Dockerfile` and
`Dockerfile_upgrade` when the larger Jupyter/Nav2/Create3 setup is needed.

You need to have Docker and docker compose installed.
It can be docker engine:
Instructions for Ubuntu are provided [here](https://docs.docker.com/engine/install/ubuntu/)

but for beginners, an easier option might be Docker Desktop: [Windows](https://docs.docker.com/desktop/install/windows-install/) [Linux](https://docs.docker.com/desktop/install/linux-install/), [Mac](https://docs.docker.com/desktop/install/mac-install/)




https://github.com/AdoHaha/ros_fun/assets/2242877/33d32bce-2f59-4905-88df-bea3bd0eb838


 I suggest cloning this repository.


`git clone https://github.com/AdoHaha/ros_fun`

`cd ros_fun`

Use 

`docker compose up ` to run the container.

Also, run 

`docker container exec -it --user ubuntu ros_fun bash -i /home/ubuntu/run_jupyter.sh`

to start jupyter inside the container.

Access the virtual machine screen by navigating to 

[http://localhost:6080](http://localhost:6080)

access the jupyter notebooks by navigating to:

[http://localhost:8888](http://localhost:8888) 

on your **host** machine. 

From there open [*exercises folder*](http://localhost:8888/exercises/1.%20introduction.ipynb) to access introduction

The demo uses ROS Humble

---

[Presentation Robot Fun with ROS2 from PyCon PL](https://www.youtube.com/watch?v=K5yGKd7ig7A)


Budowa bazy docker'a

`docker build --tag awegierska/ros2_humble:lab_mobile_ROS2_base -f Dockerfile .`

Budowa docelowej wersji

`docker build --tag awegierska/ros2_humble:lab_mobile_ROS2 -f Dockerfile_upgrade .`

Uruchomienie docker compose
'docker compose up'


Uruchomienie docker compose z X11
'docker compose -f docker-compose-x11.yml up'
