'''
from simple_pid import PID 
from time import sleep
import RPi.GPIO as GPIO


stepPin = 36
dirPin = 38
enPin = 40

kp = 0.1
ki = 0.01
kd = 0.01

pid = PID(kp, ki, kd,setpoint=100) 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(enPin, GPIO.OUT)

def control_motor(target_position):
    current_position = 0
    error_prev = 0

    while True:
        error = target_position - current_position
        output = pid(error)
        if output > 0:
            GPIO.output(dirPin, GPIO.HIGH)
        else:
            GPIO.output(dirPin, GPIO.LOW)

        for _ in range(abs(int(output))):
            GPIO.output(stepPin, GPIO.HIGH)
            sleep(0.001)
            GPIO.output(stepPin, GPIO.LOW)
            sleep(0.001)

        current_position += output

        sleep(0.1)

control_motor(100)
'''

import serial 
from time import sleep
ser = serial.Serial('/dev/ttyUSB3',115200)
try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            angles = data.split(",")
            if len(angles) == 2:
                print(f"angle_1: {angles[0]}, angle_2: {angles[1]}")
        
        sleep(0.01)

except KeyboardInterrupt:
    ser.close()