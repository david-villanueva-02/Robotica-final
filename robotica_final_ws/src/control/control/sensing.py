import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from time import sleep, time
import serial

stepPin = 36
dirPin = 38
enPin = 40
timer_start = 0
timer_end = 0

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('sensing')
        self.ser = serial.Serial('/dev/ttyACM0',115200)
        self.sensing_timer = self.create_timer(0.01,self.sensing_timer_callback)

    def sensing_timer_callback(self):
        try:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode('utf-8').rstrip()
                angles = data.split(",")
                if len(angles) == 2:
                    print(f"angle_1: {angles[0]}, angle_2: {angles[1]}")
                    
        except KeyboardInterrupt:
            self.ser.close()
            

def main(args=None) -> None:
    rclpy.init(args=args)
    node_name= NodeName()
    rclpy.spin(node_name)
    node_name.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print(e)
