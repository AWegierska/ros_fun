# Fun with ROS 2

Docker environment for ROS 2 Humble mobile robotics labs.

---

## Requirements

You need Docker and Docker Compose installed.

For Ubuntu, you can install Docker Engine using the official instructions:
[Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

For beginners, Docker Desktop may be easier:
[Windows](https://docs.docker.com/desktop/install/windows-install/),
[Linux](https://docs.docker.com/desktop/install/linux-install/),
[Mac](https://docs.docker.com/desktop/install/mac-install/)

Alternatively, you can use GitHub Codespaces.

---

## Run the Container

With X11:

```bash
docker compose -f docker-compose-x11.yml up
```

Without X11, using the browser-based desktop:

```bash
docker compose up
```

After the container starts, open:

[http://localhost:6080](http://localhost:6080)

---

## Build Docker Images

Build the base image:

```bash
docker build --tag awegierska/ros2_humble:lab_mobile_ROS2_base -f Dockerfile .
```

Build the target image:

```bash
docker build --tag awegierska/ros2_humble:lab_mobile_ROS2 -f Dockerfile_upgrade .
```

---

## Docker Images

List local Docker images:

```bash
docker images
```

Remove the project Docker images:

```bash
docker rmi awegierska/ros2_humble:lab_mobile_ROS2
docker rmi awegierska/ros2_humble:lab_mobile_ROS2_base
```

---

## Docker Containers

List all containers and check whether they are running or stopped:

```bash
docker ps -a
```

Restart the standard container:

```bash
docker restart lab_mobilne_ROS2
```

Restart the X11 container:

```bash
docker restart lab_mobilne_ROS2_x11
```

Stop and remove containers created by the standard Compose file:

```bash
docker compose down
```

Stop and remove containers created by the X11 Compose file:

```bash
docker compose -f docker-compose-x11.yml down
```

Remove the standard container manually:

```bash
docker rm lab_mobilne_ROS2
```

Remove the X11 container manually:

```bash
docker rm lab_mobilne_ROS2_x11
```
