import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
from time import sleep

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('Lazo_cerrado')
         
        # Command and info parameters, 3 is default 
        self.declare_parameter("topic_info","/R1_info")
        self.declare_parameter("topic_command","/R1")
        self.declare_parameter("referencia",90.0)
        self.declare_parameter("invertir",False)
        self.declare_parameter("tolerancia",3.0)
        self.declare_parameter("step",1.0)
        self.declare_parameter("freq",100)
        self.declare_parameter("topic_referencia","/R1_referencia")

        # Motors pins parameters, 3 is default
        self.declare_parameter("stepPin",19)
        self.declare_parameter("dirPin",21)
        self.declare_parameter("enPin",23)
        self.declare_parameter("limits",[0.0,100.0])

        # Parametros PID - por definir
        self.declare_parameter("P_PID",0.0)
        self.declare_parameter("I_PID",10000.0)
        self.declare_parameter("D_PID",0.0)

        # Pines de los motores
        self.stepPin = self.get_parameter("stepPin").value
        self.dirPin = self.get_parameter("dirPin").value
        self.enPin = self.get_parameter("enPin").value
        self.invertir = self.get_parameter("invertir").value
        self.tolerancia = self.get_parameter("tolerancia").value
        self.step = self.get_parameter("step").value
        self.periodo = 1/self.get_parameter("freq").value
        self.topic_referencia = self.get_parameter("topic_referencia").value
        
        # Pins setupt
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.stepPin, GPIO.OUT) # Pull Pin
        GPIO.setup(self.dirPin, GPIO.OUT)  # Dir Pin 
        GPIO.setup(self.enPin, GPIO.OUT)   # Enable pin 

        GPIO.output(self.enPin,False)      # Enables with value 0
        self.dir = not(self.invertir)
        GPIO.output(self.dirPin, self.dir) # Sets a direction

        self.topic_info = self.get_parameter("topic_info").value        # Sensado 
        self.topic_command = self.get_parameter("topic_command").value  # Comando
        
        self.referencia = self.get_parameter("referencia").value # Referencia a alcanzar 
        self.value = 0.0                                         # valor actual de la PV
        self.command = ""
        self.limits = self.get_parameter("limits").value         # Limites de actuacion

        self.sub_info = self.create_subscription(Float32,self.topic_info,self.info_callback,10)
        self.sub_command = self.create_subscription(String, self.topic_command,self.command_callback,10)
        self.update_referencia = self.create_subscription(Float32,self.topic_referencia,self.update_referencia,10)

        # Timer para mover la referencia 1 unidad / segundo
        self.main_timer = self.create_timer(1,self.referencia_timer_callback)

        self.PID_timer = self.create_timer(self.periodo,self.PID_timer_callback)

    def referencia_timer_callback(self): 
        if (self.command == "Aumenta" and self.referencia + self.step < self.limits[0]):
            self.referencia += self.step
        elif (self.command == "Reduce" and self.referencia - self.step > self.limits[1]):
            self.referencia -= self.step

    # Actualiza el valor de la PV
    def info_callback(self,msg):
        self.value = msg.data

    # Actualiza el comando 
    def command_callback(self,msg):
        self.command = msg.data

    # Control de posicion
    def PID_timer_callback(self):
        # Establecer margenes de error, se ponen por 3 grados/cm, por definir 
        if (not(self.value < self.referencia + self.tolerancia and self.value > self.referencia - self.tolerancia)):
            if (self.referencia > self.value and self.value < self.limits[1]):
                GPIO.output(self.dirPin, not(self.invertir))
            elif (self.referencia < self.value and self.value > self.limits[0]):
                GPIO.output(self.dirPin, self.invertir)
            GPIO.output(self.stepPin,True)
            sleep(self.periodo/2)
            GPIO.output(self.stepPin,False)

    def update_referencia(self,msg):
        self.referencia = msg.data
        
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
