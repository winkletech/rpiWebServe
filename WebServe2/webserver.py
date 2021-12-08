#!/usr/bin/python3

from flask import Flask, render_template, Response 
import picamera 
import cv2
import socket 
import io 
import os
import RPi.GPIO as GPIO
from time import sleep
import sys

cascade_path=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
face_cascade=cv2.CascadeClassifier(cascade_path)

app = Flask(__name__) 
videocapture = cv2.VideoCapture(0) 
@app.route('/') 
def index(): 
   """Video streaming .""" 
   return render_template('index.html') 
#The definition below creates the video frame by frame and adds the facial detection
def video(): 
   while True: 
       rval, frame = videocapture.read() 
       
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

       faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
        )
       
       for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

       cv2.imwrite('pic.jpg', frame)

       yield (b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n') 
#Adds the video from the above step to the webpage element
@app.route('/video_feed') 
def video_feed(): 
   return Response(video(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 

@app.route('/pan_left')
def pan_left():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    pwm = GPIO.PWM(4, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(2+(int(0)/18))
    sleep(0.5)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()
    return "nothing"

@app.route('/pan_right')
def pan_right():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    pwm = GPIO.PWM(4, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(2+(int(180)/18))
    sleep(0.5)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()
    return "nothing"


if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=False, threaded=True) 
