FROM spot_ros2_asier:latest


COPY spot_slam /ros_ws/src/spot_slam
#COPY spot_description/spot_description/urdf/accessories.urdf.xacro /ros_ws/src/spot_description/spot_description/urdf/

RUN  apt-get install -yq --no-install-recommends ros-humble-velodyne-description

WORKDIR /ros_ws
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
RUN echo "source /ros_ws/install/setup.bash" >> /root/.bashrc