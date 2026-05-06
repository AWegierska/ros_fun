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
        fluxbox \
        gedit \
        git \
        less \
        nano \
        novnc \
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
        x11vnc \
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

RUN useradd --create-home --shell /bin/bash --groups sudo vscode && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode && \
    mkdir -p /home/vscode/ros_ws/src && \
    chown -R vscode:vscode /home/vscode

RUN su - vscode -c 'for attempt in 1 2 3; do rosdep update --rosdistro humble && break; if [ "$attempt" = "3" ]; then exit 1; fi; sleep 5; done'

COPY .devcontainer/start-novnc.sh /usr/local/bin/start-novnc.sh

RUN chmod +x /usr/local/bin/start-novnc.sh && \
    printf '%s\n' \
        '<!doctype html>' \
        '<html lang="en">' \
        '<head>' \
        '  <meta charset="utf-8">' \
        '  <meta http-equiv="refresh" content="0; url=vnc_lite.html?autoconnect=true">' \
        '  <title>ROS GUI noVNC</title>' \
        '</head>' \
        '<body>' \
        '  <p>Opening <a href="vnc_lite.html?autoconnect=true">noVNC</a>...</p>' \
        '</body>' \
        '</html>' \
        > /usr/share/novnc/index.html && \
    printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        'exec sudo "${EDITOR:-nano}" /etc/bash.bashrc' \
        > /usr/local/bin/edit-system-bashrc && \
    printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        'DISPLAY="${DISPLAY:-:1}"' \
        'xterm -geometry "${1:-120x32}" -fa Monospace -fs 11 -e bash -lc "cd /workspaces/ros_fun 2>/dev/null || cd \"$HOME/ros_ws\"; exec bash -l" >/tmp/xterm-extra.log 2>&1 &' \
        > /usr/local/bin/new-gui-terminal && \
    chmod +x /usr/local/bin/edit-system-bashrc && \
    chmod +x /usr/local/bin/new-gui-terminal && \
    printf '%s\n' \
        "source /opt/ros/humble/setup.bash" \
        "[ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ] && source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" \
        "export TURTLEBOT3_MODEL=burger" \
        "export DISPLAY=\${DISPLAY:-:1}" \
        "export LIBGL_ALWAYS_SOFTWARE=1" \
        "export QT_X11_NO_MITSHM=1" \
        > /etc/profile.d/ros-humble.sh && \
    echo "source /etc/profile.d/ros-humble.sh" >> /home/vscode/.bashrc && \
    chown vscode:vscode /home/vscode/.bashrc

ENV BASH_ENV=/etc/profile.d/ros-humble.sh

USER vscode
WORKDIR /home/vscode/ros_ws

CMD ["/usr/local/bin/start-novnc.sh"]
