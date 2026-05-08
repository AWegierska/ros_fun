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
- rqt TF tree plugin,
- PlotJuggler with ROS 2 integration,
- Gazebo Classic integration with TurtleBot3 Gazebo packages,
- preloaded TSR ROS 2 example packages in `/home/vscode/tsr_workspaces/example_tsr_ws/src/`,
- `gedit` and `nano` for editing files in the VNC session,
- `pcmanfm` as a lightweight file manager in VNC,
- a lightweight `Xvfb` + `fluxbox` + `x11vnc` + noVNC desktop.

It intentionally does not install Jupyter, Chromium, the TurtleBot3
desktop metapackage, Nav2, Cartographer, Create3,
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
rqt_tf_tree
rviz2
ros2 run plotjuggler plotjuggler
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

To edit files in `common_dir/` from the noVNC desktop, use `gedit` (GUI) or
`nano` (terminal):

```bash
gedit /workspaces/ros_fun/common_dir/plik.py
nano /workspaces/ros_fun/common_dir/plik.py
```

To open PDF files in the GUI session:

```bash
evince /workspaces/ros_fun/common_dir/nazwa_pliku.pdf
```

Alternative helper command:

```bash
open-pdf /workspaces/ros_fun/common_dir/nazwa_pliku.pdf
```

In GitHub Codespaces, the most convenient option is to open PDFs directly from
the VS Code file explorer in the browser tab (native scroll + text selection +
copy/paste).

The VNC desktop includes clipboard synchronization (`autocutsel`) to improve
copy/paste between terminal windows. If needed, use the noVNC clipboard panel
(`Ctrl+Alt+Shift`) as a fallback.

Extra clipboard helper inside the container:

```bash
clip "ros2 topic list"   # copy text to CLIPBOARD
clip                     # print current CLIPBOARD content
```

In `xterm`, selected text is copied directly to clipboard. Paste with
`Ctrl+Shift+V` or middle mouse button.

Keyboard repeat is enabled in the noVNC session for smoother arrow-key
navigation (left/right/up/down hold behavior). Defaults:
- `KEY_REPEAT_DELAY=250`
- `KEY_REPEAT_RATE=35`

To verify inside the container:

```bash
xset -display :1 q
```

In GitHub Codespaces, use VS Code directly to edit files. When running locally,
you can use your own editor on the host — files are available in the mounted
project directory.

In the noVNC desktop, open Fluxbox menu with right-click. Useful shortcuts:
`Super+T` (terminal), `Super+F` (file manager), `Super+E` (`gedit`).
In `pcmanfm`, right-clicking empty space in a folder view opens a context action
for launching a terminal in that location.

To edit the system-wide Bash startup file from the noVNC terminal:

```bash
edit-system-bashrc
```

This opens `/etc/bash.bashrc` in `gedit` with sudo privileges. To edit the user Bash startup
file instead, use:

```bash
nano ~/.bashrc
```

To open additional GUI terminals inside noVNC:

```bash
new-gui-terminal
```

You can run this command multiple times to keep separate terminals for ROS
nodes.

To open the example TSR workspace:

```bash
pcmanfm ~/tsr_workspaces/example_tsr_ws
```

This workspace contains `files_to_copy/tsr_pkgs` copied into
`~/tsr_workspaces/example_tsr_ws/src` (`example_tsr_msgs`,
`example_tsr_project`). The workspace is prebuilt in the image.

The interfaces are available right after container start, for example:

```bash
ros2 interface show example_tsr_msgs/msg/ExampleMsgType
```

Rebuild manually after editing packages:

```bash
cd ~/tsr_workspaces/example_tsr_ws
colcon build
```

After building, new terminals automatically source:
`~/tsr_workspaces/example_tsr_ws/install/setup.bash`.

---

## Build Docker Image

Build the TSR image locally:

```bash
docker build --tag awegierska/ros2_humble:tsr -f .devcontainer/Dockerfile .
```

The TSR image is built directly from `.devcontainer/Dockerfile`.

Alternative Compose build command:

```bash
docker compose build
```

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

After the container starts without X11, open:

[http://localhost:6080](http://localhost:6080)

For the X11 container, open a second terminal and enter the running container:

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
rqt_tf_tree
rviz2
ros2 run plotjuggler plotjuggler
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

---

## Docker Images

List local Docker images:

```bash
docker images
```

Remove the TSR Docker image:

```bash
docker rmi awegierska/ros2_humble:tsr
```

---

## Docker Containers

List all containers and check whether they are running or stopped:

```bash
docker ps -a
```

Restart the standard TSR container:

```bash
docker restart ros_fun_tsr
```

Restart the X11 TSR container:

```bash
docker restart ros_fun_tsr_x11
```

Stop and remove containers created by the standard Compose file:

```bash
docker compose down
```

Stop and remove containers created by the X11 Compose file:

```bash
docker compose -f docker-compose-x11.yml down
```

Remove the standard TSR container manually:

```bash
docker rm ros_fun_tsr
```

Remove the X11 TSR container manually:

```bash
docker rm ros_fun_tsr_x11
```

---
