import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from std_msgs.msg import String


class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('node_name')
        print("Nodo inicializado")
        qos_profile = QoSProfile(
            reliability = ReliabilityPolicy.BEST_EFFORT,
            durability = DurabilityPolicy.TRANSIENT_LOCAL,
            history = HistoryPolicy.KEEP_LAST,
            depth = 1
        )

        # Create Publishers
     
        # Create Subscribers

        # Initialize attributes
        self.state = True

        GPIO.setmode(GPIO.BOARD) # Modo pines fisicos
        GPIO.setup(7,GPIO.OUT)
        self.timer_gpio = self.create_timer(1,self.timer_callback)
        # Create timers
    
    def timer_callback(self):
        self.state = not(self.state)
        GPIO.output(7,self.state)
    # Create callback methods (subscribers and timers)
       
def pinesCleanup():
    GPIO.cleanup(7)

def main(args=None) -> None:
    rclpy.init(args=args)
    node_name= NodeName()
    rclpy.spin(node_name)
    node_name.destroy_node()
    pinesCleanup()
    rclpy.shutdown()

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print(e)
