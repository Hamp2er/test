from std_msgs.msg import Float64
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # Наш главный герой для движения

class FigureMover(Node):
    def __init__(self):
        super().__init__('motorpins')
        self.create.publisher_()
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(Float64,"/range",self.range_callback, 10)
        self.timer_for1()
        self.declare_parameter("left_motor_pin",0)
        self.declare_parameter("right_motor_pin",1)
        leftPin = self.get_parameter('left_motor_pin').value
        rightPin = self.get_parameter('right_motor_pin').value
        self.get_logger().info(f"r motor on:{rightPin},l motor on:{leftPin}")
        self.lifetime = 0.0
    def timer_for1(self):
        self.timer = self.create_timer(0.1, self.timercallback)
    def timercallback(self):
        msg = Twist()
        msg.linear.x = self.lifetime
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.lifetime += 0.5
        msg.linear.x += 0.1
        self.get_logger().info(f"speed_increasing:"{self.lifetime})
        if msg.linear.x ==1.0:
        msg.linear.x = 0
        if self.lifetime == 1.0:
            stop.msg = Twist()
            self.publisher_.publish(stop_msg)
            self.timer.cancel()
    def range_callback(self):
        if msg.data < 0.5:
            self.get_logger().warn('wall sts close')
            self.lifetime = 0 


    
        