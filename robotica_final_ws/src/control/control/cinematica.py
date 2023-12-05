import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
import math 

L1 = 8.0
L2 = 11.0
L3 = 16.0
L4 = 6.0

class NodeName(Node):
    def __init__(self) -> None:
        super().__init__('node_name')
        print("Nodo inicializado")

        # Create Subscribers
        self.P1_value_sub = self.create_subscription(Float32,"P1_info",self.update_P1,10)
        self.P2_value_sub = self.create_subscription(Float32,"P2_info",self.update_P1,10)
        self.R1_value_sub = self.create_subscription(Float32,"R1_info",self.update_P1,10)
        self.R2_value_sub = self.create_subscription(Float32,"R2_info",self.update_P1,10)

        # Create Publishers
        self.P1_referencia_pub = self.create_publisher(Float32, "/P1_referencia", 10)
        self.P2_referencia_pub = self.create_publisher(Float32, "/P2_referencia", 10)
        self.R1_referencia_pub = self.create_publisher(Float32, "/R1_referencia", 10)
        self.R2_referencia_pub = self.create_publisher(Float32, "/R2_referencia", 10)

        self.P1_referencia = Float32()
        self.P2_referencia = Float32()
        self.R1_referencia = Float32()
        self.R2_referencia = Float32()

        self.P1_value = Float32()
        self.P2_value = Float32()
        self.R1_value = Float32()
        self.R2_value = Float32()

        while True: self.input_refs()

    def input_refs(self):
        print("Directa = 1")
        print("Inversa = 2")
        modalidad = input("Modalidad?: ")
        if modalidad == 1: #Calculo de las coordenadas de cinematica directa
            P1 = input("Valor para P1: ")
            while (P1 < 0.0 or P1 > 24.0): P1 = input("Error, valor para P1: ")
            self.P1_referencia.data = P1

            P2 = input("Valor para P2: ")
            while (P2 < 0.0 or P2 > 14.5): P1 = input("Error, valor para P2: ")
            self.P2_referencia.data = P2

            R1 = input("Valor para P2: ")
            while (R1 < -90.0 or R1 > 90.0): R1 = input("Error, valor para R1: ")
            self.P2_referencia.data = R1
            
            R2 = input("Valor para P2: ")
            while (R2 < -90.0 or R2 > 0.0): R2 = input("Error, valor para R2: ")
            self.P2_referencia.data = R2

            self.P1_referencia_pub.publish(self.P1_referencia)
            self.P2_referencia_pub.publish(self.P2_referencia)
            self.R1_referencia_pub.publish(self.R1_referencia)
            self.R2_referencia_pub.publish(self.R2_referencia)

            valid_P1 = self.P1_value.data > self.P1_referencia.data - 0.5 and self.P1_value.data < self.P1_referencia.data + 0.5
            valid_P2 = self.P2_value.data > self.P2_referencia.data - 0.5 and self.P2_value.data < self.P2_referencia.data + 0.5
            valid_R1 = self.R1_value.data > self.R1_referencia.data - 3.0 and self.R1_value.data < self.R1_referencia.data + 3.0
            valid_R2 = self.R2_value.data > self.R2_referencia.data - 3 and self.R2_value.data < self.R2_referencia.data + 3.0

            while (not(valid_P1 and valid_P2 and valid_R1 and valid_R2)):
                valid_P1 = self.P1_value.data > self.P1_referencia.data - 0.5 and self.P1_value.data < self.P1_referencia.data + 0.5
                valid_P2 = self.P2_value.data > self.P2_referencia.data - 0.5 and self.P2_value.data < self.P2_referencia.data + 0.5
                valid_R1 = self.R1_value.data > self.R1_referencia.data - 3.0 and self.R1_value.data < self.R1_referencia.data + 3.0
                valid_R2 = self.R2_value.data > self.R2_referencia.data - 3.0 and self.R2_value.data < self.R2_referencia.data + 3.0
            
            # Cinematica directa
            X = -math.sin(math.degrees(self.R1_value.data))*(L3 + L4*math.sin(math.degrees(self.R2_value.data)))
            Y = L2 + self.P1_value.data + L3*math.cos(math.degrees(self.R1_value.data)) + L4*math.cos(math.degrees(self.R1_value.data))*math.sin(math.degrees(self.R2_value.data))
            Z = L1 + self.P2_value.data - L4*math.cos(math.degrees(self.R2_value.data))

            print(f"Coordenadas: ({X}, {Y}, {Z})")

        elif modalidad == 2: #Calculo de los grados de libertad en funcion de las coordenadas
            pass
        else: print("Error")

    def update_P1(self,msg):
        self.P1_value.data = msg.data

    def update_P2(self,msg):
        self.P2_value.data = msg.data

    def update_R1(self,msg):
        self.R1_value.data = msg.data

    def update_R2(self,msg):
        self.R2_value.data = msg.data
     
    
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
