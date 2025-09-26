import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import open3d as o3d
import numpy as np
import struct

def create_pointcloud2(points, frame_id="map"):
    """
    Convert a Nx3 array to a PointCloud2 message
    """
    fields = [
        PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
    ]

    header = rclpy.time.Time().to_msg()
    msg = PointCloud2()
    msg.header.stamp = rclpy.clock.Clock().now().to_msg()
    msg.header.frame_id = frame_id
    msg.height = 1
    msg.width = len(points)
    msg.fields = fields
    msg.is_bigendian = False
    msg.point_step = 12
    msg.row_step = msg.point_step * msg.width
    msg.is_dense = True

    buffer = []
    for p in points:
        buffer.append(struct.pack('fff', *p))
    msg.data = b''.join(buffer)

    return msg


class PCDPublisher(Node):
    def __init__(self):
        super().__init__('pcd_publisher')
        self.publisher_ = self.create_publisher(PointCloud2, 'pcd_pointcloud', 10)

        # Load PCD
        pcd = o3d.io.read_point_cloud('/ros_ws/workspace/p213.pcd')
        self.points = np.asarray(pcd.points)

        # Timer to publish once (or repeatedly)
        self.timer = self.create_timer(1.0, self.publish_pointcloud)

    def publish_pointcloud(self):
        msg = create_pointcloud2(self.points, frame_id="map")
        self.publisher_.publish(msg)
        self.get_logger().info('Published point cloud')
        self.timer.cancel()  # Comment this if you want repeated publishing


def main(args=None):
    rclpy.init(args=args)
    node = PCDPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import PointCloud2
# import pcl
# import std_msgs.msg
# import sensor_msgs_py.point_cloud2 as pc2
# import os

# class PCDPublisher(Node):
#     def __init__(self):
#         super().__init__('pcd_publisher')
#         self.publisher_ = self.create_publisher(PointCloud2, '/point_cloud', 10)
#         self.timer = self.create_timer(1.0, self.publish_pcd)
#         self.get_logger().info('PCD Publisher Node Initialized')

#     def publish_pcd(self):
#         pcd_file_path = "/workspace/your_pcd_file.pcd"  # Adjust path as needed
#         if not os.path.exists(pcd_file_path):
#             self.get_logger().error(f"PCD file not found: {pcd_file_path}")
#             return

#         cloud = pcl.load(pcd_file_path)
#         pc_data = pcl_to_ros(cloud)
#         self.publisher_.publish(pc_data)
#         self.get_logger().info('Publishing PCD data')

# def pcl_to_ros(pcl_cloud):
#     pc_data = pc2.create_cloud_xyz32(std_msgs.msg.Header(), pcl_cloud.to_array())
#     return pc_data

# def main(args=None):
#     rclpy.init(args=args)
#     node = PCDPublisher()
#     rclpy.spin(node)
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()


#colcon build --packages-select pcd_simulator
#source install/setup.bash
#ros2 run pcd_simulator pcd_publisher
#Finally, once everything is set up, you can use RViz to visualize the simulated point cloud data:    
