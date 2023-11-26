import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
from time import sleep

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('Lazo_cerrado')
         
        # Command and info parameters, 1 is default 
        self.declare_parameter("topic_info","/P1_info")
        self.declare_parameter("topic_command","/P1")
        self.declare_parameter("referencia",0.0)

        # Motors pins parameters, 1 is default
        self.declare_parameter("stepPin",36)
        self.declare_parameter("dirPin",38)
        self.declare_parameter("enPin",40)
        self.declare_parameter("limits",[0,180])

        # Parametros PID - por definir
        self.declare_parameter("P_PID",0.0)
        self.declare_parameter("I_PID",10000.0)
        self.declare_parameter("D_PID",0.0)

        # Pines de los motores
        self.stepPin = self.get_parameter("stepPin").value
        self.dirPin = self.get_parameter("dirPin").value
        self.enPin = self.get_parameter("enPin").value
        self.motorTopic = self.get_parameter("motorTopic").value
        
        # Pins setupt
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.stepPin, GPIO.OUT) # Pull Pin
        GPIO.setup(self.dirPin, GPIO.OUT)  # Dir Pin 
        GPIO.setup(self.enPin, GPIO.OUT)   # Enable pin 

        GPIO.output(self.enPin,False)      # Enables with value 0
        self.dir = True
        GPIO.output(self.dirPin, self.dir) # Sets a direction

        self.topic_info = self.get_parameter("topic_info").value        # Sensado 
        self.topic_command = self.get_parameter("topic_command").value  # Comando
        
        self.referencia = self.get_parameter("referencia").value # Referencia a alcanzar 
        self.value = 0.0                                         # valor actual de la PV
        self.command = ""
        self.limits = self.get_parameter("limits").value         # Limites de actuacion

        self.sub_info = self.create_subscription(Float32,self.topic_info,self.info_callback,10)
        self.sub_command = self.create_subscription(String, self.topic_command,self.command_callback,10)

        # Timer para mover la referencia 1 unidad / segundo
        self.main_timer = self.create_timer(1,self.referencia_timer_callback)

        self.PID_timer = self.create_timer(0.01,self.PID_timer_callback,10)

    def referencia_timer_callback(self): 
        if (self.command == "Aumenta" and self.referencia + 1 < self.limits[0]):
            self.referencia += 1.0
        elif (self.command == "Reduce" and self.referencia - 1 > self.limits[1]):
            self.referencia -= 1.0

    # Actualiza el valor de la PV
    def info_callback(self,msg):
        self.value = msg.data

    # Actualiza el comando 
    def command_callback(self,msg):
        self.command = msg.data

    # Control de posicion
    def PID_timer_callback(self):

        # Establecer margenes de error, se ponen por 3 grados/cm, por definir 
        if (self.value < self.referencia + 3 or self.value > self.referencia + 3):
            if (self.referencia > self.value):
                GPIO.output(self.dirPin, True)
            elif (self.referencia < self.value):
                GPIO.output(self.dirPin, False)
            GPIO.output(self.stepPin,True)
            sleep(0.005)
            GPIO.output(self.stepPin,False)
        
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
