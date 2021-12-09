#!/usr/bin/python3

from flask import Flask, render_template, Response, jsonify, request, redirect, url_for
import picamera 
import cv2
import socket 
import io 
import os
import RPi.GPIO as GPIO
from time import sleep
import sys

#Sets the path for the facial recognition data

cascade_path=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
face_cascade=cv2.CascadeClassifier(cascade_path)

#Initiates flask

app = Flask(__name__) 
videocapture = cv2.VideoCapture(0) 
@app.route('/') 
def index(): 
    return render_template('final_index.html') 
#The definition below creates the video frame by frame and adds the facial detection
def video(): 
    while True: 
        rval, frame = videocapture.read() 

#Converts the images to grayscale for facial recognition
       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#Parameters for facial detection

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
            )
       
#Draws a green square around the faces detected

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

#Writes the image as 'pic.jpg' to be opened below

        cv2.imwrite('pic.jpg', frame)

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + open('/home/pi/cv_env/WebServe2/pic.jpg', 'rb').read() + b'\r\n') 

#Adds the video from the above step to the webpage element

@app.route('/video_feed') 
def video_feed(): 
    return Response(video(), mimetype='multipart/x-mixed-replace; boundary=frame') 

#Takes the value from the pan slider and moves the servo to that location
    
@app.route('/pan_slider')
def pan():
    pan_val = request.args.get('pan_val')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    pwm_pan = GPIO.PWM(4, 50)
    pwm_pan.start(0)
    pwm_pan.ChangeDutyCycle(2+(int(pan_val)/18))
    sleep(0.5)
    pwm_pan.ChangeDutyCycle(0)
    pwm_pan.stop()
    GPIO.cleanup()
    return(pan_val)

#Takes the value from the tilt slider and moves the servo to that location

@app.route('/tilt_slider')
def tilt():
    tilt_val = request.args.get('slide_val2')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)
    pwm_tilt = GPIO.PWM(23, 50)
    pwm_tilt.start(0)
    pwm_tilt.ChangeDutyCycle(2+(int(tilt_val)/18))
    sleep(0.5)
    pwm_tilt.ChangeDutyCycle(0)
    pwm_tilt.stop()
    GPIO.cleanup
    return(tilt_val)

if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=False, threaded=True) 
