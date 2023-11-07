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

        timer_start = time()
        self.main_timer = self.create_timer(1,self.callback_main_timer)

    def callback_main_timer(self): # 1 step - 200 steps = 1 turn
        GPIO.output(stepPin,False)
        sleep(0.5)
        GPIO.output(stepPin,True)
        timer_end = time()
        tiempo = timer_end - timer_start
        print(str(tiempo))
        
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
