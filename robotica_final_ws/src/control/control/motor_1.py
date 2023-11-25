import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from time import sleep, time

# Motor 1 - P1
stepPin = 36 
dirPin = 38  
enPin = 40   

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('nodo_motor_1')
        print("Nodo inicializado")
        GPIO.setmode(GPIO.BOARD)
        
        self.step_counter = 0
        self.dir = "" # Direccion como string recibido del publiser

        # Pines del motor 1
        GPIO.setup(stepPin, GPIO.OUT) # Pull Pin
        GPIO.setup(dirPin, GPIO.OUT)  # Dir Pin - controls direction
        GPIO.setup(enPin, GPIO.OUT)   # Enable pin 

        GPIO.output(enPin,False)      # Enables with value 0
        GPIO.output(dirPin, True)

        self.subscriber_P1 = self.create_subscription(String, "/P1", self.callback_P1,10)
        self.main_timer = self.create_timer(0.01,self.callback_main_timer)
    
    def callback_P1(self,msg):
        self.dir = msg.data
        if self.dir == "Aumenta":
            GPIO.output(dirPin, True)
        elif self.dir == "Reduce":
            GPIO.output(dirPin, False)
        
        if self.dir == "":
            GPIO.output(enPin,True)
        else:
            GPIO.output(enPin,False)

    def callback_main_timer(self): 
        GPIO.output(stepPin,GPIO.HIGH)
        sleep(0.005)
        GPIO.output(stepPin, GPIO.LOW)

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
