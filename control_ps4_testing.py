import pygame
import time 

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Error")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("COntroler de PS4 detectado: {}".format(joystick.get_name()))

    try:
        while True:

            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if (event.axis == 0 or event.axis == 3):
                            print("Eje {}: {}".format(event.axis, event.value))
                elif event.type == pygame.JOYBUTTONDOWN:
                    print("Boton presionado: {}".format(event.button))
                elif event.type == pygame.JOYBUTTONUP:
                    print("Boton liberado: {}".format(event.button))
                elif event.type == pygame.JOYHATMOTION:
                    print("HAT direction: {}".format(event.value))

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Programa terminado por el usuario.")
    finally:
        joystick.quit()
        pygame.quit()