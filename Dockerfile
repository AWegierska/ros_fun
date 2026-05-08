FROM tiryoh/ros2-desktop-vnc:humble
LABEL maintainer="wegierska.agnieszka@gmail.com"
# based on https://github.com/AdoHaha/ros_fun/tree/master

ENV USER=root
# Aktualizacja i instalacja pakietów systemowych
RUN apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    apt-get autoclean && \
    apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update -q && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        python3-pip \
        ros-humble-cartographer \
        ros-humble-cartographer-ros \
        ros-humble-nav2-bringup \
        ros-humble-gazebo-* \
        ros-humble-dynamixel-sdk \
        ros-humble-test-msgs \
        ros-humble-rqt-tf-tree \
        ros-humble-plotjuggler-ros \
        ros-humble-turtle-tf2-py \
        ros-humble-tf2-ros \ 
        ros-humble-tf2-tools \
        ros-humble-turtlesim \
        python3-zmq \
        chromium-browser \
        lcov \
        gedit nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Aktualizacja pip i instalacja pakietów Pythona
RUN pip3 install --upgrade pip && \
    pip3 install -U \
        "setuptools<80" \
        notebook \
        jupyterlab \
        jupyterlab-rise \
        opencv-contrib-python \
        bqplot \
        tornado==6.1 \
        --ignore-installed flask && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV USER=ubuntu
ARG COLCON_PARALLEL_WORKERS=8
ENV CMAKE_BUILD_PARALLEL_LEVEL=${COLCON_PARALLEL_WORKERS}
ENV MAKEFLAGS=-j${COLCON_PARALLEL_WORKERS}

# Kopiowanie niezbędnych plików
RUN mkdir -p /home/ubuntu/ros_ws/src
COPY ./files_to_copy/jupyter_notebooks/rviz_nav.rviz /opt/ros/humble/share/nav2_bringup/rviz/nav2_default_view.rviz
ADD ./files_to_copy/jupyter_notebooks /home/ubuntu/ros_ws/src/jupyter_notebooks
RUN cd /home/ubuntu/ros_ws && . /opt/ros/humble/setup.sh && colcon build --symlink-install --parallel-workers ${COLCON_PARALLEL_WORKERS}

#from https://ubuntu.com/blog/simulate-the-turtlebot3
RUN mkdir -p /home/ubuntu/turtlebot3_ws/src
COPY ./files_to_copy/run_jupyter.sh /home/ubuntu/run_jupyter.sh
COPY ./files_to_copy/jupyter_notebook_config.py /home/ubuntu/.jupyter/jupyter_notebook_config.py

RUN cd /home/ubuntu/turtlebot3_ws/src && git clone -b humble https://github.com/ros-planning/navigation2.git
RUN cd /home/ubuntu/turtlebot3_ws && source /opt/ros/humble/setup.sh && rosdep install -y -r -q --from-paths src --ignore-src --rosdistro humble

RUN cd /home/ubuntu/turtlebot3_ws/src && git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git && git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3.git && git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
RUN cd /home/ubuntu/turtlebot3_ws && . /opt/ros/humble/setup.sh && colcon build --symlink-install --parallel-workers ${COLCON_PARALLEL_WORKERS}

RUN mkdir -p /home/ubuntu/tsr_workspaces/example_tsr_ws/src
ADD ./files_to_copy/tsr_pkgs/ /home/ubuntu/tsr_workspaces/example_tsr_ws/src
RUN cd /home/ubuntu/tsr_workspaces/example_tsr_ws && . /opt/ros/humble/setup.sh && colcon build --symlink-install --parallel-workers ${COLCON_PARALLEL_WORKERS}
