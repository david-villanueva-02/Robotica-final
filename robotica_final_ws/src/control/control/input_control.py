import rclpy
import pygame
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
        super().__init__('input_control')
        self.get_counter = pygame.joystick.get_count(0)

        self.P1 = self.create_publisher(String,"/P1",10)
        self.P2 = self.create_publisher(String,"/P2",10)
        self.R1 = self.create_publisher(String,"/R1",10)
        self.R2 = self.create_publisher(String,"/R2",10)
        self.message_move = String()
        self.message_move.data = ""

        if self.get_counter == 0:
            print("Control no encontrado")
        else:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            try:
                self.main_timer = self.create_timer(0.001, self.callback_timer1)
            except KeyboardInterrupt:
                print("Programa terminado")
            finally:
                self.joystick.quit()
                pygame.quit()
    

    def callback_timer1(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                match event.axis:
                    case 1:
                        if event.value > 0.8:
                            self.message_move.data = "Reduce"
                        elif event.value < -0.8:
                            self.message_move.data = "Aumenta"
                        else: self.message_move.data = ""
                        self.R1.publish(self.message_move)
                        break
                    case 4:
                        if event.value > 0.8:
                            self.message_move.data = "Reduce"
                        elif event.value < -0.8:
                            self.message_move.data = "Aumenta"
                        else: self.message_move.data = ""
                        self.R1.publish(self.message_move)
                        break

            elif event.type == pygame.JOYBUTTONDOWN:
                print("Boton presionado: {}".format(event.button))
            elif event.type == pygame.JOYBUTTONUP:
                print("Boton liberado: {}".format(event.button))
            elif event.type == pygame.JOYHATMOTION:
                P1 = event.button[0]
                P2 = event.button[1]
                match P1:
                    case -1:
                        self.message_move.data = "Reduce"
                        break
                    case 1:
                        self.message_move.data = "Aumenta"
                        break
                    case 0: 
                        self.message_move.data = ""
                        break
                self.P1.publish(self.message_move)
                match P2:
                    case -1:
                        self.message_move.data = "Reduce"
                        break
                    case 1:
                        self.message_move.data = "Aumenta"
                        break
                    case 0:
                        self.message_move.data = ""
                        break
                self.P2.publish(self.message_move)
                

def main(args=None) -> None:
    pygame.init()
    pygame.joystick.init()
    rclpy.init(args=args)
    node_name= NodeName()
    rclpy.spin(node_name)
    node_name.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Programa terminado")
