#!/usr/bin/python3

import os
import RPi.GPIO as GPIO
from time import sleep
import sys

def move():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    pwm = GPIO.PWM(4, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(2+(int(0)/18))
    sleep(0.5)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()

move()

