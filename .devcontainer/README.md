# .devcontainer — ROS 2 Humble TSR

This directory contains the devcontainer configuration used by both
**GitHub Codespaces** and local **Docker Compose** runs.

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Image definition based on `ros:humble-ros-base-jammy` |
| `devcontainer.json` | Codespaces configuration (ports, env vars, VS Code extensions) |
| `start-novnc.sh` | Container CMD: starts the full VNC+noVNC desktop |

## Dockerfile

Base image: `ros:humble-ros-base-jammy`

**Installs:**
- ROS 2 packages: turtlesim, Gazebo, TurtleBot3, RViz2, rqt, colcon, rosdep, vcstool
- GUI stack: Xvfb, fluxbox, x11vnc, novnc, websockify, xterm
- Editors: gedit, nano
- Dev tools: git, build-essential, cmake, curl, python3-pip

**Creates user** `vscode` with passwordless sudo.

**Helper scripts** installed to `/usr/local/bin/`:
- `start-novnc.sh` — container entrypoint
- `new-gui-terminal` — open additional xterm window in VNC
- `edit-system-bashrc` — edit `/etc/bash.bashrc` with sudo nano

**ROS environment** sourced automatically via `/etc/profile.d/ros-humble.sh`.

## start-novnc.sh — How noVNC Works

```
Xvfb :1 (virtual display 1600x900)
  └─ fluxbox (window manager)
  └─ xterm (initial terminal, cd /workspaces/ros_fun)
  └─ x11vnc (VNC server on port 5901)
        └─ websockify (WebSocket bridge on port 6080)
              └─ noVNC web client → http://localhost:6080
```

The noVNC `index.html` auto-redirects to `vnc_lite.html?autoconnect=true`.

## devcontainer.json

- **Port forwarded**: `6080` (noVNC desktop)
- **Remote user**: `vscode`
- **Workspace**: `/workspaces/<repo-name>`
- **VS Code extensions**: Python, C++, ROS

## Usage

### GitHub Codespaces

1. Push `tsr` branch to GitHub
2. Open repo → Code → Codespaces → Create codespace on `tsr`
3. Wait for build
4. Open `Ports` tab → click port `6080` for VNC desktop
5. Use VS Code terminal for ROS commands, VNC desktop for GUI apps

### Local — noVNC

```bash
docker compose up --build
# open http://localhost:6080
```

### Local — X11 (Linux hosts only)

```bash
docker compose -f docker-compose-x11.yml up --build
docker compose -f docker-compose-x11.yml exec ros2 bash
```

## Editing Files

| Context | Tool |
|---------|------|
| VNC session | `gedit` (GUI) or `nano` (terminal) |
| Codespaces | VS Code editor |
| Local machine | Any host editor — project is volume-mounted |

Files in `common_dir/` are accessible inside the container at
`/workspaces/ros_fun/common_dir/`.

## Example ROS Commands (run in terminal)

```bash
ros2 run turtlesim turtlesim_node
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
rviz2
rqt_graph
```
