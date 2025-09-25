import os
import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='spot_ros2',
            executable='spot_driver',  # Adjust as necessary
            name='spot_driver',
            output='screen',
            parameters=[],
            remappings=[]
        ),
        # Simulate a PointCloud2 publisher node for visualization
        Node(
            package='your_package',  # Replace with your package that simulates point cloud
            executable='pcd_publisher',  # Your PCD publisher node
            name='pcd_publisher',
            output='screen'
        )
    ])
