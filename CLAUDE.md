# CLAUDE.md — ROS Fun Docker Project

## Project Overview

Educational Docker environment for learning ROS 2 Humble. Students use it during
robotics lab sessions. The environment runs either locally or via GitHub Codespaces.

## Branch Structure

- `tsr` — active development branch (current lightweight setup)
- `ROS_1_mobilne` — main/stable branch

## Key Files

| File | Purpose |
|------|---------|
| `.devcontainer/Dockerfile` | Main image definition (used by both compose files and Codespaces) |
| `.devcontainer/devcontainer.json` | GitHub Codespaces configuration |
| `.devcontainer/start-novnc.sh` | Container startup: Xvfb + fluxbox + x11vnc + websockify |
| `docker-compose.yml` | Local noVNC mode (port 6080) |
| `docker-compose-x11.yml` | Local X11 forwarding mode |
| `common_dir/` | Teaching materials and student files (mounted as volume) |
| `Dockerfile`, `Dockerfile_upgrade` | Legacy full images — do not modify without explicit request |

## Container Details

- **Base image**: `ros:humble-ros-base-jammy`
- **User**: `vscode` (has passwordless sudo)
- **Workdir**: `/home/vscode/ros_ws`
- **Project mount**: `.` → `/workspaces/ros_fun`
- **common_dir inside container**: `/workspaces/ros_fun/common_dir/`
- **TSR packages inside container**: `/home/vscode/ros_ws/src/` (copied from `files_to_copy/tsr_pkgs/`)

## Installed ROS Packages

- `ros-humble-turtlesim`
- `ros-humble-gazebo-ros-pkgs`
- `ros-humble-turtlebot3-gazebo`, `ros-humble-turtlebot3-msgs`
- `ros-humble-rviz2`
- `ros-humble-rqt`, `ros-humble-rqt-common-plugins`
- `python3-colcon-common-extensions`, `python3-rosdep`, `python3-vcstool`

## Build & Run

```bash
# noVNC (local or Codespaces)
docker compose up --build
# → open http://localhost:6080

# X11 forwarding (Linux host only)
docker compose -f docker-compose-x11.yml up --build
docker compose -f docker-compose-x11.yml exec ros2 bash

# Build image only
docker build -f .devcontainer/Dockerfile -t ros-fun-tsr-humble .
```

## Helper Commands (inside container)

- `new-gui-terminal` — open additional xterm in VNC session
- `edit-system-bashrc` — edit `/etc/bash.bashrc` with sudo nano

## Fluxbox Desktop Ergonomics

- Right-click on desktop opens the fluxbox menu with:
  - Terminal, File Manager (`pcmanfm`), Gedit
  - quick links to `TSR_instrukcje` and `/home/vscode/ros_ws/src`
  - ROS launchers (`turtlesim`, `rviz2`, `rqt`, `rqt_graph`, TurtleBot3 Gazebo)
- Keyboard shortcuts:
  - `Super+T` -> terminal
  - `Super+F` -> file manager
  - `Super+E` -> gedit
- Toolbar is enabled at the bottom with window list and clock.

## File Editing

- **VNC session**: `gedit` (GUI), `pcmanfm` (browse files), or `nano` (terminal)
- **Codespaces**: VS Code editor directly
- **Local**: use host editor — files are in the mounted project directory

## Not Installed (intentional)

Jupyter, Chromium, Nav2, Cartographer, PlotJuggler, Create3, Ignition/Fortress, RMF, full Ubuntu desktop.
