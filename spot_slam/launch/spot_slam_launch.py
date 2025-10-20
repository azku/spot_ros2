from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='spot_slam',
            executable='pointcloud_transformer',
            name='pointcloud_transformer',
            output='screen',
            parameters=[{'use_sim_time': False}],
        )
    ])
