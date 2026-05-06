#!/usr/bin/env bash
# Note: no set -e so background process failures don't abort the script

export DISPLAY="${DISPLAY:-:1}"
export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}"
export QT_X11_NO_MITSHM="${QT_X11_NO_MITSHM:-1}"
export TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-burger}"

# Clean up stale X lock files
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1
mkdir -p /tmp/.X11-unix
chmod 1777 /tmp/.X11-unix

# Start virtual framebuffer
Xvfb "$DISPLAY" -screen 0 1600x900x24 -ac +extension GLX +render -noreset &
sleep 2

# Set background colour
xsetroot -display "$DISPLAY" -solid '#2e3436' || true

# Start window manager
DISPLAY="$DISPLAY" fluxbox >/tmp/fluxbox.log 2>&1 &
sleep 1

# Start initial terminal
DISPLAY="$DISPLAY" xterm -geometry 120x32+40+40 \
    -title "ROS 2 Humble terminal" \
    -fa Monospace -fs 11 \
    -e bash -lc 'cd /workspaces/ros_fun 2>/dev/null || cd "$HOME/ros_ws"; echo "Use new-gui-terminal to open another GUI terminal."; echo "Use edit-system-bashrc to edit /etc/bash.bashrc."; exec bash -l' \
    >/tmp/xterm.log 2>&1 &

# Start VNC server — loop to restart if it crashes
(while true; do
    x11vnc -display "$DISPLAY" -forever -shared -nopw \
        -listen 0.0.0.0 -rfbport 5901 \
        -noxdamage -noscr -nowf \
        >>/tmp/x11vnc.log 2>&1
    echo "x11vnc exited, restarting in 2s..." >> /tmp/x11vnc.log
    sleep 2
done) &

# Wait for x11vnc to open port 5901
for i in $(seq 1 15); do
    if grep -q 'PORT=5901' /tmp/x11vnc.log 2>/dev/null; then
        break
    fi
    sleep 1
done

# Start noVNC websocket bridge
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
