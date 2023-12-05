import RPi.GPIO as GPIO
import rclpy
from time import time, sleep
from rclpy.node import Node
from std_msgs.msg import String

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('node_name')
        print("Nodo inicializado")

        # Create Publishers
     
        # Create Subscribers
        self.actuador_command = self.create_subscription(String,"/Actuador",self.actuador_command_update,10)

        GPIO.setmode(GPIO.BOARD) # Modo pines fisicos
        GPIO.setup(32,GPIO.OUT)  # Salida PWM para el servo

        self.pwm = GPIO.PWM(32,50)
        self.pwm.start(0)

    def actuador_command_update(self,msg):
        if msg.data == "Abrir":
            self.set_angle(0)
        elif msg.data == "Cerrar":
            self.set_angle(90)

    def set_angle(self,angle):
        duty = angle / 18 + 2
        GPIO.output(32,True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(32,False)
        self.pwm.ChangeDutyCycle(0)
       
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
