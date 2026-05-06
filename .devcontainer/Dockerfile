FROM ros:humble-ros-base-jammy

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV DISPLAY=:1
ENV LIBGL_ALWAYS_SOFTWARE=1
ENV QT_X11_NO_MITSHM=1
ENV TURTLEBOT3_MODEL=burger
ENV GAZEBO_MODEL_PATH=/opt/ros/humble/share/turtlebot3_gazebo/models

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash-completion \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        autocutsel \
        evince \
        fluxbox \
        gedit \
        git \
        less \
        nano \
        novnc \
        pcmanfm \
        python3-colcon-common-extensions \
        python3-pip \
        python3-rosdep \
        python3-vcstool \
        ros-humble-gazebo-ros-pkgs \
        ros-humble-rqt \
        ros-humble-rqt-common-plugins \
        ros-humble-rviz2 \
        ros-humble-turtlebot3-gazebo \
        ros-humble-turtlebot3-msgs \
        ros-humble-turtlesim \
        sudo \
        websockify \
        x11-xserver-utils \
        xclip \
        xsel \
        x11vnc \
        xdg-utils \
        xfonts-base \
        xterm \
        xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then \
        rosdep init; \
    fi && \
    for attempt in 1 2 3; do \
        rosdep update --rosdistro humble && break; \
        if [ "$attempt" = "3" ]; then exit 1; fi; \
        sleep 5; \
    done

RUN mkdir -p /tmp/.X11-unix && \
    chown root:root /tmp/.X11-unix && \
    chmod 1777 /tmp/.X11-unix

RUN useradd --create-home --shell /bin/bash --groups sudo vscode && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode && \
    mkdir -p /home/vscode/ros_ws/src && \
    mkdir -p /home/vscode/tsr_workspaces/example_tsr_ws/src && \
    chown -R vscode:vscode /home/vscode

RUN su - vscode -c 'for attempt in 1 2 3; do rosdep update --rosdistro humble && break; if [ "$attempt" = "3" ]; then exit 1; fi; sleep 5; done'

COPY files_to_copy/tsr_pkgs/ /home/vscode/tsr_workspaces/example_tsr_ws/src/
COPY .devcontainer/start-novnc.sh /usr/local/bin/start-novnc.sh

RUN chmod +x /usr/local/bin/start-novnc.sh && \
    printf '%s\n' \
        '<!doctype html>' \
        '<html lang="en">' \
        '<head>' \
        '  <meta charset="utf-8">' \
        '  <meta http-equiv="refresh" content="0; url=vnc.html?autoconnect=true&resize=remote&reconnect=true">' \
        '  <title>ROS GUI noVNC</title>' \
        '</head>' \
        '<body>' \
        '  <p>Opening <a href="vnc.html?autoconnect=true&resize=remote&reconnect=true">noVNC</a>...</p>' \
        '</body>' \
        '</html>' \
        > /usr/share/novnc/index.html && \
    printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        'exec sudo -E gedit /etc/bash.bashrc' \
        > /usr/local/bin/edit-system-bashrc && \
    printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        'DISPLAY="${DISPLAY:-:1}"' \
        'xterm -geometry "${1:-120x32}" -fa Monospace -fs 11 -e bash -lc "cd /workspaces/ros_fun/common_dir 2>/dev/null || cd /workspaces/ros_fun 2>/dev/null || cd \"$HOME/ros_ws\"; exec bash -l" >/tmp/xterm-extra.log 2>&1 &' \
        > /usr/local/bin/new-gui-terminal && \
    printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        'if [ "$#" -ne 1 ]; then' \
        '  echo "Usage: open-pdf /path/to/file.pdf" >&2' \
        '  exit 2' \
        'fi' \
        'exec evince "$1"' \
        > /usr/local/bin/open-pdf && \
    printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        'if [ "$#" -eq 0 ]; then' \
        '  xclip -selection clipboard -o' \
        'else' \
        '  printf "%s" "$*" | xclip -selection clipboard -in' \
        'fi' \
        > /usr/local/bin/clip && \
    chmod +x /usr/local/bin/edit-system-bashrc && \
    chmod +x /usr/local/bin/new-gui-terminal && \
    chmod +x /usr/local/bin/open-pdf && \
    chmod +x /usr/local/bin/clip && \
    mkdir -p /home/vscode/.fluxbox && \
    mkdir -p /home/vscode/.config && \
    printf '%s\n' \
        '[Default Applications]' \
        'application/pdf=org.gnome.Evince.desktop;evince.desktop;' \
        > /home/vscode/.config/mimeapps.list && \
    printf '%s\n' \
        '[begin] (ROS 2 TSR)' \
        '  [exec] (Terminal) {xterm -fa Monospace -fs 11 -geometry 120x32 -e bash -l}' \
        '  [exec] (File Manager) {pcmanfm /workspaces/ros_fun/common_dir}' \
        '  [exec] (PDF Viewer) {evince}' \
        '  [exec] (Gedit) {gedit}' \
        '  [exec] (Clipboard Tool) {xterm -fa Monospace -fs 11 -e bash -lc '\''echo "Use: clip \"text\"  (copy), clip  (paste)"; exec bash -l'\''}' \
        '  [separator]' \
        '  [exec] (Instrukcje TSR) {pcmanfm /workspaces/ros_fun/common_dir/TSR_instrukcje}' \
        '  [exec] (Pakiety TSR) {pcmanfm /home/vscode/tsr_workspaces/example_tsr_ws/src}' \
        '  [separator]' \
        '  [submenu] (ROS 2 Tools)' \
        '    [exec] (Turtlesim) {ros2 run turtlesim turtlesim_node}' \
        '    [exec] (RViz2) {rviz2}' \
        '    [exec] (rqt) {rqt}' \
        '    [exec] (rqt_graph) {rqt_graph}' \
        '    [exec] (Gazebo TurtleBot3) {ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py}' \
        '  [end]' \
        '  [separator]' \
        '  [exec] (Edit .bashrc) {xterm -fa Monospace -fs 11 -e bash -lc '\''edit-system-bashrc; exec bash -l'\''}' \
        '  [restart] (Restart Fluxbox)' \
        '[end]' \
        > /home/vscode/.fluxbox/menu && \
    printf '%s\n' \
        'session.screen0.toolbar.tools: clock, prevwindow, nextwindow, iconbar, systemtray' \
        'session.screen0.toolbar.height: 24' \
        'session.screen0.toolbar.visible: true' \
        'session.screen0.toolbar.placement: BottomCenter' \
        > /home/vscode/.fluxbox/init && \
    printf '%s\n' \
        '# Quick launchers' \
        'Mod4 t :Exec xterm -fa Monospace -fs 11 -geometry 120x32 -e bash -l' \
        'Mod4 f :Exec pcmanfm /workspaces/ros_fun/common_dir' \
        'Mod4 e :Exec gedit' \
        > /home/vscode/.fluxbox/keys && \
    printf '%s\n' \
        "source /opt/ros/humble/setup.bash" \
        "[ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ] && source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" \
        "[ -f /home/vscode/tsr_workspaces/example_tsr_ws/install/setup.bash ] && source /home/vscode/tsr_workspaces/example_tsr_ws/install/setup.bash" \
        "export TURTLEBOT3_MODEL=burger" \
        "export DISPLAY=\${DISPLAY:-:1}" \
        "export LIBGL_ALWAYS_SOFTWARE=1" \
        "export QT_X11_NO_MITSHM=1" \
        > /etc/profile.d/ros-humble.sh && \
    chown -R vscode:vscode /home/vscode/tsr_workspaces && \
    chown -R vscode:vscode /home/vscode/.fluxbox && \
    chown -R vscode:vscode /home/vscode/.config && \
    echo "source /etc/profile.d/ros-humble.sh" >> /home/vscode/.bashrc && \
    chown vscode:vscode /home/vscode/.bashrc

ENV BASH_ENV=/etc/profile.d/ros-humble.sh

USER vscode
WORKDIR /home/vscode/ros_ws

CMD ["/usr/local/bin/start-novnc.sh"]
