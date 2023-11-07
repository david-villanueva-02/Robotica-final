import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from time import sleep, time

stepPin = 36
dirPin = 38
enPin = 40
timer_start = 0
timer_end = 0

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('node_name')
        print("Nodo inicializado")
        GPIO.setmode(GPIO.BOARD)
        

        self.step_counter = 0

        # Pines del motor 1
        GPIO.setup(stepPin, GPIO.OUT) # Pull Pin
        GPIO.setup(dirPin, GPIO.OUT)  # Dir Pin - controls direction
        GPIO.setup(enPin, GPIO.OUT)   # Enable pin 

        GPIO.output(enPin,False)      # Enables with value 0
        GPIO.output(dirPin, True)

        self.main_timer = self.create_timer(0.001,self.callback_main_timer)

    def callback_main_timer(self): # 1 step - 200 steps = 1 turn
        if (self.step_counter == 3200): 
            GPIO.output(dirPin, False)
            self.step_counter = 0
        GPIO.output(stepPin,True)
        sleep(0.0005)
        GPIO.output(stepPin,False)
        self.step_counter += 1

        print("step")

        
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
