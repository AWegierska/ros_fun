# Specification: ROS Fun Docker Environment

## Purpose

Lightweight educational environment for learning ROS 2 Humble during robotics
lab sessions. Designed to minimize image size while providing all tools needed
for turtlesim and TurtleBot3 Gazebo exercises.

## Deployment Modes

| Mode | Command | Access |
|------|---------|--------|
| Local noVNC | `docker compose up` | http://localhost:6080 |
| Local X11 | `docker compose -f docker-compose-x11.yml up` | Host display (Linux only) |
| GitHub Codespaces | Automatic build from `.devcontainer/` | Port 6080 forwarded + VS Code |

## Installed Software

### ROS 2 (Humble)
- `ros2` CLI
- `colcon` build tool
- `rosdep` dependency manager
- `vcstool`
- `turtlesim`
- Gazebo Classic + `ros-humble-gazebo-ros-pkgs`
- TurtleBot3 simulation (`ros-humble-turtlebot3-gazebo`, `ros-humble-turtlebot3-msgs`)
- RViz2 (`ros-humble-rviz2`)
- rqt + common plugins (`ros-humble-rqt`, `ros-humble-rqt-common-plugins`)

### GUI Desktop (noVNC)
- Xvfb virtual framebuffer (1600x900)
- Fluxbox window manager
- Fluxbox right-click menu with ROS tools shortcuts
- Fluxbox toolbar with window list (bottom)
- x11vnc VNC server (port 5901)
- websockify + noVNC web client (port 6080)
- xterm terminal emulator
- pcmanfm file manager

### Editors
- `gedit` — graphical editor, available in VNC session
- `nano` — terminal editor

### Development Tools
- `git`, `build-essential`, `cmake`, `curl`, `bash-completion`, `python3-pip`

## User Requirements

| Requirement | Solution |
|-------------|----------|
| Open multiple terminals in VNC | `new-gui-terminal` command |
| Edit `.bashrc` | `edit-system-bashrc` (opens `/etc/bash.bashrc`) or `nano ~/.bashrc` |
| Edit files in `common_dir/` via VNC | `gedit` or `nano` |
| Browse shared folders in VNC | `pcmanfm /workspaces/ros_fun/common_dir` |
| Access preloaded ROS 2 teaching packages | `/home/vscode/ros_ws/src` (`example_tsr_msgs`, `example_tsr_project`) |
| Edit files locally | Host editor (volume mount) |
| Edit files in Codespaces | VS Code editor |

## Volumes

| Host path | Container path | Purpose |
|-----------|----------------|---------|
| `./common_dir` | `/workspaces/ros_fun/common_dir` | Shared teaching files and student work |

## Environment Variables (container)

| Variable | Value |
|----------|-------|
| `DISPLAY` | `:1` (noVNC) or `${DISPLAY}` (X11) |
| `LIBGL_ALWAYS_SOFTWARE` | `1` |
| `QT_X11_NO_MITSHM` | `1` |
| `TURTLEBOT3_MODEL` | `burger` |
| `RMW_IMPLEMENTATION` | `rmw_fastrtps_cpp` |
| `LRM_numer_stanowiska` | configurable (`.env` or shell export) |

## Intentionally Not Installed

Jupyter, Chromium, gedit-alternatives (Codium/VSCodium), Nav2, Cartographer,
PlotJuggler, Create3 simulation, Ignition/Fortress Gazebo, RMF, full Ubuntu
desktop metapackage, MATE session.
