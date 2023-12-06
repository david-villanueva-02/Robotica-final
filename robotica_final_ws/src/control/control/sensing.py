import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from time import sleep, time
import serial

stepPin = 36
dirPin = 38
enPin = 40

''' sensores sonicos
Sensor || TRIG || ECHO
1         13      15
2         16      18
'''

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('Sensing')
        self.ser = serial.Serial('/dev/ttyUSB0',115200)  # Se puede parametrizar el puerto, revisar 
        self.valor_R1 = Float32()
        self.valor_P1 = Float32()
        self.valor_P2 = Float32()
        self.valor_R2 = Float32()

        self.valor_P1.data = 0.0
        self.valor_P2.data = 0.0
        self.valor_R1.data = 0.0
        self.valor_R2.data = 0.0

        GPIO.setmode(GPIO.BOARD)

        # Sensor 1 para P1
        GPIO.setup(13,GPIO.OUT) # TRIG 1
        GPIO.setup(15,GPIO.IN)  # ECHO 1

        # Sensor 2
        GPIO.setup(16,GPIO.OUT) # TRIG 2
        GPIO.setup(18,GPIO.IN)  # ECHO 2

        # Publishers de la info de los sensores
        self.pub_P1 = self.create_publisher(Float32, "/P1_info", 10)
        self.pub_P2 = self.create_publisher(Float32, "/P2_info", 10)
        self.pub_R1 = self.create_publisher(Float32, "/R1_info", 10)
        self.pub_R2 = self.create_publisher(Float32, "/R2_info", 10)

        self.arduino_timer = self.create_timer(0.01,self.arduino_timer_callback)
        self.sensor1_timer = self.create_timer(0.01,self.sensor_timer_callback_1)
        self.sensor2_timer = self.create_timer(0.01,self.sensor_timer_callback_2)

        #self.timer_show = self.create_timer(1,self.show_params)

    def show_params(self):
        print(f"P1: {self.valor_P1.data}")
        print(f"P2: {self.valor_P2.data}")
        print(f"R1: {self.valor_R1.data}")
        print(f"R1: {self.valor_R2.data}")

    # Recibe informacion de un arduino
    def arduino_timer_callback(self):
        try:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode('utf-8').rstrip()
                angles = data.split(",")
                if len(angles) == 2:
                    # Conversion al angulo real 
                    #self.valor_R1.data = float(angles[0]) 
                    self.valor_R1.data = 12.43*(float(angles[0])+10) - 623.66
                    self.pub_R1.publish(self.valor_R1)

                    self.valor_R2.data = float(angles[1])*90/100*(-1)
                    self.pub_R2.publish(self.valor_R2)
                    
                    # Imprimir los angulos
                    # self.get_logger().info(f"angle_1: {angles[0]}, angle_2: {angles[1]}")
                    
        except KeyboardInterrupt:
            self.ser.close()

    # Lee la distancia de los sensores ultrasonicos
    def sensor_timer_callback_1(self):
        trigpin = 13
        echopin = 15
         
        # Se lanza el pulso 
        GPIO.output(trigpin,True)
        sleep(0.00001)
        GPIO.output(trigpin,False)
         
        # Se lee el tiempo
        while (not(GPIO.input(echopin))) : pulse_start = time()
        while(GPIO.input(echopin)): pulse_end = time()
        pulse_dur = pulse_end - pulse_start
        
        # Se publica segun el sensor 
        self.valor_P1.data = pulse_dur*34300/2
        self.pub_P1.publish(self.valor_P1)
        print(self.valor_P1.data)

    def sensor_timer_callback_2(self):
        trigpin = 16
        echopin = 18
        
        # Se lanza el pulso 
        GPIO.output(trigpin,True)
        sleep(0.00001)
        GPIO.output(trigpin,False)
         
        # Se lee el tiempo
        while (not(GPIO.input(echopin))) : pulse_start = time()
        while(GPIO.input(echopin)): pulse_end = time()
        pulse_dur = pulse_end - pulse_start
        
        # Se publica segun el sensor 
        self.valor_P2.data = pulse_dur*34300/2
        self.pub_P2.publish(self.valor_P2)
        print(self.valor_P2.data)
        
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
