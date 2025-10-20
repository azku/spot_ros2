from setuptools import find_packages, setup

package_name = 'spot_slam'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/spot_slam_launch.py']),
    ],
    install_requires=['setuptools', 'rclpy', 'sensor_msgs', 'tf2_ros', 'tf2_sensor_msgs'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pointcloud_transformer = spot_slam.pointcloud_transformer:main'
        ],
    },
)
