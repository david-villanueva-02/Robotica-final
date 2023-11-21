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

        if self.get_counter == 0:
            print("Control no encontrado")
        else:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            try:
                self.main_timer = self.create_timer(0.01, self.callback_timer1)
            except KeyboardInterrupt:
                print("Programa terminado")
            finally:
                self.joystick.quit()
                pygame.quit()
    

    def callback_timer1(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                print("Eje {}: {}".format(event.axis, event.value))
                match event.axis:
                    case 1:
                        break
                
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Boton presionado: {}".format(event.button))
            elif event.type == pygame.JOYBUTTONUP:
                print("Boton liberado: {}".format(event.button))
            elif event.type == pygame.JOYHATMOTION:
                print("HAT direction: {}".format(event.value))

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
