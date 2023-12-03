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
        self.get_counter = pygame.joystick.get_count()

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
                while True: self.main_cycle()
            except KeyboardInterrupt:
                print("Programa terminado")
            finally:
                self.joystick.quit()
                pygame.quit()

    def main_cycle(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.value > 0.8:
                    self.message_move.data = "Reduce"
                elif event.value < -0.8:
                    self.message_move.data = "Aumenta"
                else: self.message_move.data = ""

                match event.axis:
                    case 0: # Prismatico 1
                        self.P1.publish(self.message_move)
                    case 3: # Revolute 1
                        self.R1.publish(self.message_move)
                    case 1: # Prismatico 2
                        self.P2.publish(self.message_move)
                    case 4: # Revolute 2
                        self.R2.publish(self.message_move)
                if event.value > 0.8 or event.value < -0.8:
                    print(f"{event.axis}: {event.value}")

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
    finally:
        pygame.quit()
