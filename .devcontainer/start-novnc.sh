#!/usr/bin/env bash
set -euo pipefail

export DISPLAY="${DISPLAY:-:1}"
export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}"
export QT_X11_NO_MITSHM="${QT_X11_NO_MITSHM:-1}"
export TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-burger}"

rm -f /tmp/.X1-lock /tmp/.X11-unix/X1
mkdir -p /tmp/.X11-unix

Xvfb "$DISPLAY" -screen 0 1600x900x24 -ac +extension GLX +render -noreset &
sleep 1

fluxbox >/tmp/fluxbox.log 2>&1 &
xterm -geometry 120x32+40+40 \
    -title "ROS 2 Humble terminal" \
    -fa Monospace \
    -fs 11 \
    -e bash -lc 'cd /workspaces/ros_fun 2>/dev/null || cd "$HOME/ros_ws"; exec bash -l' &
x11vnc -display "$DISPLAY" -forever -shared -nopw -listen 0.0.0.0 -rfbport 5901 >/tmp/x11vnc.log 2>&1 &

if [ -d /usr/share/novnc ]; then
    NOVNC_WEB=/usr/share/novnc
else
    NOVNC_WEB=/usr/share/novnc/web
fi

websockify --web="$NOVNC_WEB" 0.0.0.0:6080 localhost:5901 >/tmp/novnc.log 2>&1 &

echo "noVNC is available on forwarded port 6080."
echo "Try: ros2 run turtlesim turtlesim_node"
echo "Try: ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py"

exec sleep infinity
