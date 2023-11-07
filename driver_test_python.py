import RPi.GPIO as GPIO
from std_msgs.msg import String
from time import sleep

stepPin = 36
dirPin = 38
enPin = 40

def Girar():
    GPIO.output(enPin,True)      # Enables with value 0
    for x in range(400):
        GPIO.output(stepPin,True)
        sleep(0.001)
        GPIO.output(stepPin,False)
        sleep(0.001)
        print("step "+str(x)) 
    print("Changind direction...")
    sleep(1)

    GPIO.output(enPin,False)      # Enables with value 0
    for x in range(400):
        GPIO.output(stepPin,True)
        sleep(0.001)
        GPIO.output(stepPin,False)
        sleep(0.001)
        print("step "+str(x)) 
    print("Changind direction...")
    sleep(1)
    
GPIO.setmode(GPIO.BOARD)

# Pines del motor 1
GPIO.setup(stepPin, GPIO.OUT) # Pull Pin
GPIO.setup(dirPin, GPIO.OUT)  # Dir Pin - controls direction
GPIO.setup(enPin, GPIO.OUT)   # Enable pin 

GPIO.output(dirPin, True)

while(True): Girar()

