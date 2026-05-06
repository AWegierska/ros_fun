#!/usr/bin/env bash
set -u

export DISPLAY="${DISPLAY:-:1}"
export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}"
export QT_X11_NO_MITSHM="${QT_X11_NO_MITSHM:-1}"
export TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-burger}"
export KEY_REPEAT_DELAY="${KEY_REPEAT_DELAY:-250}"
export KEY_REPEAT_RATE="${KEY_REPEAT_RATE:-35}"

touch /tmp/x11vnc.log /tmp/fluxbox.log /tmp/xterm.log
touch /tmp/start-novnc.trace
echo "[start] $(date -Is)" >> /tmp/start-novnc.trace

# Clean up stale X lock file
rm -f /tmp/.X1-lock
rm -f /tmp/.X11-unix/X1 2>/dev/null || true

# Ensure X11 socket directory exists (non-blocking, no sudo prompt risk)
mkdir -p /tmp/.X11-unix || true
chmod 1777 /tmp/.X11-unix 2>/dev/null || true

# Start virtual framebuffer
echo "[step] start Xvfb" >> /tmp/start-novnc.trace
Xvfb "$DISPLAY" -screen 0 1600x900x24 -ac +extension GLX +render -noreset &
sleep 2
if ! pgrep -f "Xvfb $DISPLAY" >/dev/null 2>&1; then
    echo "ERROR: Xvfb did not start on $DISPLAY"
    exit 1
fi

# Set background colour
echo "[step] xsetroot" >> /tmp/start-novnc.trace
xsetroot -display "$DISPLAY" -solid '#2e3436' || true

# Enable keyboard auto-repeat with native-like timing for arrow keys in noVNC.
echo "[step] keyboard repeat" >> /tmp/start-novnc.trace
xset -display "$DISPLAY" r on || true
xset -display "$DISPLAY" r rate "$KEY_REPEAT_DELAY" "$KEY_REPEAT_RATE" || true

# Start window manager
echo "[step] start fluxbox" >> /tmp/start-novnc.trace
DISPLAY="$DISPLAY" fluxbox >/tmp/fluxbox.log 2>&1 &
sleep 1

# Keep PRIMARY and CLIPBOARD in sync for better copy/paste in VNC
echo "[step] start autocutsel" >> /tmp/start-novnc.trace
timeout 2s env DISPLAY="$DISPLAY" autocutsel -fork >/tmp/autocutsel-clipboard.log 2>&1 || true
timeout 2s env DISPLAY="$DISPLAY" autocutsel -selection PRIMARY -fork >/tmp/autocutsel-primary.log 2>&1 || true

# Start initial terminal
echo "[step] start xterm" >> /tmp/start-novnc.trace
DISPLAY="$DISPLAY" xterm -geometry 120x32+40+40 \
    -title "ROS 2 Humble terminal" \
    -fa Monospace -fs 11 \
    -e bash -lc 'cd /workspaces/ros_fun/common_dir 2>/dev/null || cd /workspaces/ros_fun 2>/dev/null || cd "$HOME/ros_ws"; echo "Right-click on desktop for Fluxbox menu."; echo "Shortcuts: Super+T terminal, Super+F file manager, Super+E gedit."; echo "Use new-gui-terminal to open another GUI terminal."; echo "Use edit-system-bashrc to edit /etc/bash.bashrc."; exec bash -l' \
    >/tmp/xterm.log 2>&1 &

# Start VNC server
echo "[step] start x11vnc" >> /tmp/start-novnc.trace
x11vnc -display "$DISPLAY" -forever -shared -nopw \
    -repeat \
    -listen 0.0.0.0 -rfbport 5901 \
    -noxdamage -noscr -nowf \
    >>/tmp/x11vnc.log 2>&1 &
sleep 1
if ! ps -ef | grep -v grep | grep -q "x11vnc -display $DISPLAY"; then
    echo "ERROR: x11vnc did not stay running. Check /tmp/x11vnc.log"
    tail -n 120 /tmp/x11vnc.log || true
    exit 1
fi

# Give x11vnc a brief head-start, but do not block startup on log pattern matching
sleep 1

# Start noVNC websocket bridge
echo "[step] detect novnc web root" >> /tmp/start-novnc.trace
if [ -f /usr/share/novnc/vnc.html ]; then
    NOVNC_WEB=/usr/share/novnc
elif [ -f /usr/share/novnc/web/vnc.html ]; then
    NOVNC_WEB=/usr/share/novnc/web
else
    echo "Cannot find noVNC web root (vnc.html)."
    echo "Checked: /usr/share/novnc and /usr/share/novnc/web"
    ls -la /usr/share/novnc 2>/dev/null || true
    exit 1
fi

echo "Using noVNC web root: $NOVNC_WEB"
echo "noVNC should be available on forwarded port 6080."
echo "Use right mouse button on desktop to open Fluxbox menu."
echo "Shortcuts: Super+T terminal, Super+F file manager, Super+E gedit."
echo "Try: ros2 run turtlesim turtlesim_node"
echo "Try: ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py"
echo "Starting websockify in foreground..."
echo "[step] start websockify" >> /tmp/start-novnc.trace
if ! command -v websockify >/dev/null 2>&1; then
    echo "ERROR: websockify command is missing."
    exit 1
fi
exec websockify --web="$NOVNC_WEB" 0.0.0.0:6080 localhost:5901
