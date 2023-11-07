import RPi.GPIO as GPIO
from std_msgs.msg import String
from time import sleep



def Girar(stepPin, step_counter):
    GPIO.output(stepPin,False)
    sleep(0.0005)
    GPIO.output(stepPin,True)
    sleep(0.0005)
    step_counter +=1
    print("step "+str(step_counter)) 
    return step_counter
    
def main():

    stepPin = 36
    dirPin = 38
    enPin = 40
    step_counter = 0
   

    GPIO.setmode(GPIO.BOARD)

    # Pines del motor 1
    GPIO.setup(stepPin, GPIO.OUT) # Pull Pin
    GPIO.setup(dirPin, GPIO.OUT)  # Dir Pin - controls direction
    GPIO.setup(enPin, GPIO.OUT)   # Enable pin 

    GPIO.output(enPin,False)      # Enables with value 0
    GPIO.output(dirPin, True)

    while(True): step_counter = Girar(stepPin,step_counter)

if __name__ == "__main__":
    main()