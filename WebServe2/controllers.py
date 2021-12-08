#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys


def servo_base_control(starting_point, change):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(23,GPIO.OUT)
    servo = GPIO.PWM(23,50) #the first number is the pin and the second is the pulse in Hz, 50Hz

    #This sets the servo start point at 0
    servo.start(0)

    #This cycles through the inputs from the user to adjust the servo accordingly
    try:
        while True:
            angle = int(input("Enter the angle of Rotation: "))

            servo.ChangeDutyCycle(2+(float(angle)/18))
            time.sleep(0.5)
            servo.ChangeDutyCycle(0)
            break

    finally:
        servo.stop()
        GPIO.cleanup()


def servo_clamp_control(starting_point, change):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(4,GPIO.OUT)
    servo = GPIO.PWM(4,50) #the first number is the pin and the second is the pulse in Hz, 50Hz

    #This sets the servo start point at 0
    servo.start(0)

    #This cycles through the inputs from the user to adjust the servo accordingly
    try:
        while True:
            angle = int(input("Enter the angle of tilt: "))

            servo.ChangeDutyCycle(2+(float(angle)/18))
            time.sleep(0.5)
            servo.ChangeDutyCycle(0)
            break

    finally:
        servo.stop()
        GPIO.cleanup()

#**********************Main body of the program***************************
#user_b = 0
#user_c = 0

rotate_move = 90
tilt_move = 90
tilt_change_pos = 10
rotate_change_pos = 10
tilt_change_neg = -10
rotate_change_neg = -10

while True:
       servo_clamp_control(90,0)
        








#    if keyboard.press_and_release('a'):
#        print("working")


    #if keyboard.is_pressed("a") or keyboard.is_pressed("d"):
    #    servo_base_control(user_b + 10)

    #if keyboard.is_pressed("w") or keyboard.is_pressed("s"):
    #    servo_clamp_control(user_c + 10)

    #change = input()
    
#while True:
 #   servo_clamp_control(0)
  #  servo_clamp_control(180)
