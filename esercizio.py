import rclpy
from rclpy.node import Node
from sysmonitor_interfaces.msg import Sysmon
import random
from std_msgs.msg import Float64
import sys

class myNode(Node):
    def __init__(self):
        super().__init__('mynode')
        self.publisher_=self.create_publisher(Float64,'/test',10)
        timer=0.5
        self.timer_call=self.create_timer(timer,self.func)
    def func(self):
        sysmon_msg = Sysmon()
        sysmon_msg.cpu_usage = random.uniform(0, 100)
        msg=Float64()
        msg.data=sysmon_msg.cpu_usage
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing CPU usage:{msg.data} %')
if __name__=='__main__':
    rclpy.init()
    mynode=myNode()
    rclpy.spin(mynode)
    print('Mannagg tutt cos')
    mynode.destroy_node()
    rclpy.shutdown()