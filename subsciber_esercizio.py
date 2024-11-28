import rclpy
from rclpy.node import Node
from sysmonitor_interfaces.msg import Sysmon
import random
from std_msgs.msg import Float64
import sys
import rosbag2_py

class Subscriber(Node):
    def __init__(self):
        super().__init__('sub')
        self.subscription=self.create_subscription(
            Sysmon,
            'test',
            self.listener_callback,
            10
        )
        self.subscription

    def listener_callback(self,msg):
        new_msg=Sysmon()
        new_msg.cpu_usage=msg.cpu_usage
        new_msg.cpu_temp=msg.cpu_temp
        new_msg.gpu_usage=msg.gpu_usage
        new_msg.gpu_temp=msg.gpu_temp
        new_msg.gpuram_usage=msg.gpuram_usage
        self.get_logger().info(f'I received a {new_msg.cpu_usage} % of usage of cpu')
        self.get_logger().info(f'I received a {new_msg.cpu_temp} degree from cpu')
        self.get_logger().info(f'I received a {new_msg.gpu_usage} % of usage of gpu')
        self.get_logger().info(f'I received a {new_msg.cpu_temp} degree from gpu')
        self.get_logger().info(f'I received a {new_msg.cpu_usage} % of usage of gpuram')
        
def main():
    rclpy.init()
    sub=Subscriber()
    rclpy.spin(sub)
    sub.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
