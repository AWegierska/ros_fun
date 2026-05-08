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
        lxterminal \
        nano \
        novnc \
        pcmanfm \
        python3-colcon-common-extensions \
        python3-pip \
        python3-rosdep \
        python3-vcstool \
        ros-humble-gazebo-ros-pkgs \
        ros-humble-plotjuggler-ros \
        ros-humble-rqt \
        ros-humble-rqt-common-plugins \
        ros-humble-rqt-tf-tree \
        ros-humble-rviz2 \
        ros-humble-tf2-ros \
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
        zip \
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

RUN chown -R vscode:vscode /home/vscode/tsr_workspaces && \
    su - vscode -c 'source /opt/ros/humble/setup.bash && cd /home/vscode/tsr_workspaces/example_tsr_ws && colcon build --symlink-install'

RUN chmod +x /usr/local/bin/start-novnc.sh && \
    printf '%s\n' \
        '<!doctype html>' \
        '<html lang="en">' \
        '<head>' \
        '  <meta charset="utf-8">' \
        '  <meta http-equiv="refresh" content="0; url=vnc.html?autoconnect=true&resize=scale&reconnect=true">' \
        '  <title>ROS GUI noVNC</title>' \
        '</head>' \
        '<body>' \
        '  <p>Opening <a href="vnc.html?autoconnect=true&resize=scale&reconnect=true">noVNC</a>...</p>' \
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
        'lxterminal --no-remote --geometry="${1:-120x32}" --working-directory="/workspaces/ros_fun/common_dir" --command="bash -lc '\''exec bash -l'\''" >/tmp/lxterminal-extra.log 2>&1 &' \
        > /usr/local/bin/new-gui-terminal && \
    printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        'target_dir="${1:-$HOME}"' \
        'if ! cd "$target_dir" 2>/dev/null; then' \
        '  cd /workspaces/ros_fun/common_dir 2>/dev/null || cd "$HOME"' \
        'fi' \
        'exec lxterminal --no-remote --geometry=120x32 --working-directory="$PWD" --command="bash -lc '\''exec bash -l'\''"' \
        > /usr/local/bin/open-gui-terminal-here && \
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
    chmod +x /usr/local/bin/open-gui-terminal-here && \
    chmod +x /usr/local/bin/open-pdf && \
    chmod +x /usr/local/bin/clip && \
    mkdir -p /home/vscode/.fluxbox && \
    mkdir -p /home/vscode/.config && \
    mkdir -p /home/vscode/.local/share/file-manager/actions && \
    printf '%s\n' \
        '[Default Applications]' \
        'application/pdf=org.gnome.Evince.desktop;evince.desktop;' \
        > /home/vscode/.config/mimeapps.list && \
    printf '%s\n' \
        '[Desktop Entry]' \
        'Type=Action' \
        'Name=Open in Terminal' \
        'Comment=Open terminal in the current folder' \
        'Icon=utilities-terminal' \
        'TargetLocation=true' \
        'MimeType=inode/directory;' \
        'SelectionCount=0' \
        'Exec=/usr/local/bin/open-gui-terminal-here %d' \
        > /home/vscode/.local/share/file-manager/actions/open-terminal-here.desktop && \
    printf '%s\n' \
        '[begin] (ROS 2 TSR)' \
        '  [exec] (Terminal) {lxterminal --no-remote --geometry=120x32 --working-directory=/workspaces/ros_fun/common_dir --command="bash -lc '\''exec bash -l'\''"}' \
        '  [exec] (common_dir) {pcmanfm /workspaces/ros_fun/common_dir}' \
        '  [exec] (PDF Viewer) {evince}' \
        '  [exec] (Gedit) {gedit}' \
        '  [separator]' \
        '  [exec] (Instrukcje TSR) {pcmanfm /workspaces/ros_fun/common_dir/TSR_instrukcje}' \
        '  [exec] (Przykladowy workspace TSR) {pcmanfm /home/vscode/tsr_workspaces/example_tsr_ws}' \
        '  [separator]' \
        '  [submenu] (ROS 2 Tools)' \
        '    [exec] (Turtlesim) {ros2 run turtlesim turtlesim_node}' \
        '    [exec] (RViz2) {rviz2}' \
        '    [exec] (rqt) {rqt}' \
        '    [exec] (rqt_graph) {rqt_graph}' \
        '    [exec] (rqt_tf_tree) {ros2 run rqt_tf_tree rqt_tf_tree}' \
        '    [exec] (PlotJuggler) {ros2 run plotjuggler plotjuggler}' \
        '    [exec] (Gazebo TurtleBot3) {ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py}' \
        '  [end]' \
        '  [separator]' \
        '  [exec] (Edit .bashrc) {lxterminal --no-remote --geometry=120x32 --working-directory=/workspaces/ros_fun/common_dir --command="bash -lc '\''edit-system-bashrc; exec bash -l'\''"}' \
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
        'Mod4 t :Exec lxterminal --no-remote --geometry=120x32 --working-directory=/workspaces/ros_fun/common_dir --command="bash -lc '\''exec bash -l'\''"' \
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
        "export PS1='\${debian_chroot:+(\$debian_chroot)}\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ '" \
        > /etc/profile.d/ros-humble.sh && \
    chown -R vscode:vscode /home/vscode/tsr_workspaces && \
    chown -R vscode:vscode /home/vscode/.fluxbox && \
    chown -R vscode:vscode /home/vscode/.config && \
    chown -R vscode:vscode /home/vscode/.local && \
    echo "source /etc/profile.d/ros-humble.sh" >> /home/vscode/.bashrc && \
    chown vscode:vscode /home/vscode/.bashrc

ENV BASH_ENV=/etc/profile.d/ros-humble.sh

USER vscode
WORKDIR /home/vscode/ros_ws

CMD ["/usr/local/bin/start-novnc.sh"]
