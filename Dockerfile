FROM adohaha/fun_ros:ros1
LABEL maintainer wegierska.agnieszka@gmail.com

RUN mkdir /usr/share/processing
ADD processing-3.5.4 /usr/share/processing/processing-3.5.4
ADD processing.desktop /home/ubuntu/Desktop/processing.desktop
ADD sketchbook /home/ubuntu/sketchbook
ADD jupyter.sh /home/ubuntu/Desktop/jupyter.sh

RUN apt-get --yes install ros-noetic-rosbridge-server
RUN git clone https://github.com/AWegierska/pkg_rob_usl.git /home/ubuntu/catkin_ws/src/pkg_rob_usl

WORKDIR /home/ubuntu/catkin_ws/src/multirobot_nav
RUN git pull
COPY setup.bash /home/ubuntu/setup.bash
RUN ["/bin/bash", "-c", "/home/ubuntu/setup.bash"]
