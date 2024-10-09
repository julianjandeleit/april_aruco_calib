FROM ros:noetic


# install prerequisites
RUN apt-get update && apt-get install -y \
      git software-properties-common python3-vcstool python3-catkin-tools python3-osrf-pycommon 

#RUN add-apt-repository --remove ppa:bernd-pfrommer/gtsam && apt-add-repository --remove ppa:borglab/gtsam-release-4.0

RUN  apt-add-repository ppa:borglab/gtsam-release-4.1 && apt update && apt install -y libgtsam-dev libgtsam-unstable-dev && \
      rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
      ros-noetic-image-transport \
      ros-noetic-image-geometry \
      ros-noetic-cv-bridge \
      ros-noetic-tf2-ros \
      ros-noetic-tf2-geometry-msgs \
      ros-noetic-tf \
      libopencv-dev

# RUN apt-get update && apt-get install -y \
#       ros-noetic-catkin \
#       python3-catkin-tools

# note that setup.sh works but setup.bash not
RUN . /opt/ros/noetic/setup.sh && \
    cd ~ && git clone https://github.com/berndpfrommer/tagslam_root.git && \
    cd ~/tagslam_root &&\
    vcs import --recursive < tagslam_root.repos && \
    catkin config -DCMAKE_BUILD_TYPE=RelWithDebInfo && \
    catkin build

# visualization and tools
RUN apt-get install -y ros-noetic-rviz tmux eog

# launch ros package
# CMD ["ros2", "launch", "demo_nodes_cpp", "talker_listener_launch.py"]
CMD ["bash"]
