import rclpy
from rclpy.serialization import deserialize_message
from rclpy.node import Node
from sysmonitor_interfaces.msg import Sysmon
import rosbag2_py

class Publisher(Node):
    def __init__(self):
        super().__init__('pub')
        self.publisher_=self.create_publisher(Sysmon,'test',10)
        timer=0.1
        self.path='/home/mich/ros2_ws/rosbag2_2024_11_22-00_32_31/rosbag2_2024_11_22-00_32_31_0.mcap'
        self.bag_reader=self.initialize_bag_reader()
        self.timer=self.create_timer(timer,self.callback)

    def initialize_bag_reader(self):
        storage_options=rosbag2_py.StorageOptions(uri=self.path,storage_id='mcap')
        converter_options=rosbag2_py.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
        reader = rosbag2_py.SequentialReader()
        reader.open(storage_options, converter_options)
        return reader

    def callback(self):
        while self.bag_reader.has_next():
            topic,data,timestamp=self.bag_reader.read_next()
            if topic=='/system_info':
                self.get_logger().info(f'Received a message from {topic}')
                msg=deserialize_message(data,Sysmon)
                new_msg=Sysmon()
                new_msg.cpu_temp=msg.cpu_temp
                new_msg.cpu_usage=msg.cpu_usage
                new_msg.gpu_usage=msg.gpu_usage
                new_msg.gpu_temp=msg.gpu_temp
                new_msg.ram_usage=msg.ram_usage
                new_msg.gpuram_usage=msg.gpuram_usage
                self.publisher_.publish(new_msg)
                self.get_logger().info(f'Published: {new_msg.cpu_temp}'+  
                                   f' {new_msg.cpu_usage}%'+ 
                                   f' {new_msg.gpu_usage}%'+
                                   f' {new_msg.gpu_temp}'+
                                   f' {new_msg.ram_usage}%'+
                                   f' {new_msg.gpuram_usage}%')
def main():
    rclpy.init()
    pub=Publisher()
    rclpy.spin(pub)
    pub.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
