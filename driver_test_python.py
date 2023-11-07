import RPi.GPIO as GPIO
from std_msgs.msg import String
from time import sleep

stepPin = 36
dirPin = 38
enPin = 40
dir = False

def Girar():
    for x in range(400):
        GPIO.output(stepPin,True)
        sleep(0.01)
        GPIO.output(stepPin,False)
        sleep(0.01)
        print("step "+str(x)) 
    sleep(1)
    print("Changind direction...")
    dir = not(dir)
    GPIO.output(enPin,dir)      # Enables with value 0
    
GPIO.setmode(GPIO.BOARD)

# Pines del motor 1
GPIO.setup(stepPin, GPIO.OUT) # Pull Pin
GPIO.setup(dirPin, GPIO.OUT)  # Dir Pin - controls direction
GPIO.setup(enPin, GPIO.OUT)   # Enable pin 

GPIO.output(enPin,dir)      # Enables with value 0
GPIO.output(dirPin, True)

while(True): Girar()

