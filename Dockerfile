# Use official Ubuntu 22.04 base image
FROM ros:humble-ros-base

# Env setup
ENV SHELL=/bin/bash
SHELL ["/bin/bash", "-c"]

# Set up workspace
WORKDIR /ros_ws/src

# Initialize rosdep
# RUN rosdep init && rosdep update

# Clone driver code
RUN git clone https://github.com/bdaiinstitute/spot_ros2.git .
RUN git submodule update --init --recursive

# Run install script and pass in the architecture
RUN ARCH=$(dpkg --print-architecture) && echo "Building driver with $ARCH" && /ros_ws/src/install_spot_ros2.sh --$ARCH

# Build packages with Colcon
WORKDIR /ros_ws/
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install
