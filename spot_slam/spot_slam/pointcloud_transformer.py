import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from tf2_ros import Buffer, TransformListener
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
from geometry_msgs.msg import TransformStamped

class PointCloudTransformer(Node):
    def __init__(self):
        super().__init__('pointcloud_transformer')

        # Initialize the transform buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Subscriber to the point cloud topic
        self.pointcloud_subscriber = self.create_subscription(
            PointCloud2,
            '/spot/sensor_origin_velodyne_point_cloud',  # Original topic from Spot SDK
            self.pointcloud_callback,
            10
        )

        # Publisher for the transformed point cloud
        self.pointcloud_publisher = self.create_publisher(
            PointCloud2,
            'spot/transformed_velodyne_point_cloud',  # New topic
            10
        )

    def pointcloud_callback(self, msg):
        # Try to get the transform from odom to the desired frame (e.g., base_link)
        try:
            transform = self.tf_buffer.lookup_transform(
                'base_link',  # Target frame
                '/spot/odom', #Source frame
                #msg.header.frame_id,  # Source frame (from the incoming point cloud)
                rclpy.time.Time()
            )
            # Transform the point cloud
            transformed_cloud = do_transform_cloud(msg, transform)

            # Publish the transformed point cloud
            self.pointcloud_publisher.publish(transformed_cloud)

        except Exception as e:
            self.get_logger().error(f'Error transforming point cloud: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = PointCloudTransformer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
