import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from time import sleep

# Motor 1 - P1
'''
stepPin = 36 
dirPin = 38  
enPin = 40   
motorTopic = "/P1"
'''

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('nodo_motor_1')
        print("Nodo inicializado")

        # Parametros para cada motor
        self.declare_parameter("stepPin",36)
        self.declare_parameter("dirPin",38)
        self.declare_parameter("enPin",40)
        self.declare_parameter("motorTopic","/P1")

        self.stepPin = self.get_parameter("stepPin").value
        self.dirPin = self.get_parameter("dirPin").value
        self.enPin = self.get_parameter("enPin").value
        self.motorTopic = self.get_parameter("motorTopic").value
        
        GPIO.setmode(GPIO.BOARD)
        
        self.step_counter = 0
        self.dir = "" # Direccion como string recibido del publiser

        # Pines del motor n - de los parametros
        GPIO.setup(self.stepPin, GPIO.OUT) # Pull Pin
        GPIO.setup(self.dirPin, GPIO.OUT)  # Dir Pin - controls direction
        GPIO.setup(self.enPin, GPIO.OUT)   # Enable pin 

        GPIO.output(self.enPin,False)      # Enables with value 0
        GPIO.output(self.dirPin, True)

        self.subscriber_P1 = self.create_subscription(String, self.motorTopic, self.callback_P1,10)
        self.main_timer = self.create_timer(0.01,self.callback_main_timer)
    
    def callback_P1(self,msg):
        self.dir = msg.data
        if self.dir == "Aumenta":
            GPIO.output(self.dirPin, True)
        elif self.dir == "Reduce":
            GPIO.output(self.dirPin, False)
        
        if self.dir == "":
            GPIO.output(self.enPin,True)
        else:
            GPIO.output(self.enPin,False)

    def callback_main_timer(self): 
        GPIO.output(self.stepPin,True)
        sleep(0.005)
        GPIO.output(self.stepPin, False)

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
