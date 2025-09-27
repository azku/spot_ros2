import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import open3d as o3d
import numpy as np
import struct
import tf2_ros
import geometry_msgs.msg
from rclpy.time import Time

def create_pointcloud2(points, frame_id="map"):
    """
    Convert a Nx3 array to a PointCloud2 message.
    """
    fields = [
        PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
    ]

    # Get current time and set the header
    header = rclpy.clock.Clock().now().to_msg()

    msg = PointCloud2()
    msg.header.stamp = header
    msg.header.frame_id = "map"
    msg.height = 1  # For unorganized point clouds (flat)
    msg.width = len(points)  # Number of points
    msg.fields = fields
    msg.is_bigendian = False
    msg.point_step = 12  # 3 floats (x, y, z)
    msg.row_step = msg.point_step * msg.width
    msg.is_dense = True

    # Convert points to binary data
    buffer = []
    for p in points:
        buffer.append(struct.pack('fff', *p))
    msg.data = b''.join(buffer)

    return msg


class PCDPublisher(Node):
    def __init__(self):
        super().__init__('pcd_publisher')
        self.publisher_ = self.create_publisher(PointCloud2, 'pcd_pointcloud', 10)

        # Initialize the Transform Broadcaster
        self.broadcaster = tf2_ros.TransformBroadcaster(self)

        # Load PCD
        pcd = o3d.io.read_point_cloud('/ros_ws/workspace/route3_ss05.pcd')
        
        # Debugging: Check if points are loaded correctly
        if pcd.is_empty():
            self.get_logger().error("Failed to load point cloud!")
        else:
            self.points = np.asarray(pcd.points)  # Get the point data as a numpy array
            self.get_logger().info(f"Loaded point cloud with {len(self.points)} points.")
        
        # Timer to publish point cloud periodically
        self.timer = self.create_timer(1.0, self.publish_pointcloud)

    def broadcast_transform(self):
        # Define the transform from 'world' to 'map'
        transform = geometry_msgs.msg.TransformStamped()
        
        # Time-stamp the transform
        transform.header.stamp = self.get_clock().now().to_msg()
        
        # The transform is from the 'world' frame to the 'map' frame
        transform.header.frame_id = 'world'  # Parent frame (world)
        transform.child_frame_id = 'map'     # Child frame (map)

        # Set translation (modify as needed)
        transform.transform.translation.x = 0.0
        transform.transform.translation.y = 0.0
        transform.transform.translation.z = 0.0
        
        # Set rotation (identity rotation in this example)
        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        transform.transform.rotation.w = 1.0

        # Broadcast the transform
        self.broadcaster.sendTransform(transform)
        self.get_logger().info("Broadcasted transform from world to map")

    def publish_pointcloud(self):
        if hasattr(self, 'points') and len(self.points) > 0:
            msg = create_pointcloud2(self.points, frame_id="map")
            self.publisher_.publish(msg)
            self.get_logger().info('Published point cloud')
            self.broadcast_transform()  # Broadcast transform with each point cloud message
        else:
            self.get_logger().warn("No point cloud data to publish")


def main(args=None):
    rclpy.init(args=args)
    node = PCDPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
