import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import pcl
import std_msgs.msg
import sensor_msgs_py.point_cloud2 as pc2
import os

class PCDPublisher(Node):
    def __init__(self):
        super().__init__('pcd_publisher')
        self.publisher_ = self.create_publisher(PointCloud2, '/point_cloud', 10)
        self.timer = self.create_timer(1.0, self.publish_pcd)
        self.get_logger().info('PCD Publisher Node Initialized')

    def publish_pcd(self):
        pcd_file_path = "/workspace/your_pcd_file.pcd"  # Adjust path as needed
        if not os.path.exists(pcd_file_path):
            self.get_logger().error(f"PCD file not found: {pcd_file_path}")
            return

        cloud = pcl.load(pcd_file_path)
        pc_data = pcl_to_ros(cloud)
        self.publisher_.publish(pc_data)
        self.get_logger().info('Publishing PCD data')

def pcl_to_ros(pcl_cloud):
    pc_data = pc2.create_cloud_xyz32(std_msgs.msg.Header(), pcl_cloud.to_array())
    return pc_data

def main(args=None):
    rclpy.init(args=args)
    node = PCDPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


#colcon build --packages-select pcd_simulator
#source install/setup.bash
#ros2 run pcd_simulator pcd_publisher
#Finally, once everything is set up, you can use RViz to visualize the simulated point cloud data:    
