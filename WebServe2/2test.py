#!/usr/bin/python3

from flask import Flask, render_template, Response 
import picamera 
import cv2
import socket 
import io 
import os

cascade_path=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
face_cascade=cv2.CascadeClassifier(cascade_path)

app = Flask(__name__) 
videocapture = cv2.VideoCapture(0) 
@app.route('/') 
def index(): 
   """Video streaming .""" 
   return render_template('index.html') 
def gen(): 
   """Video streaming generator function.""" 
   while True: 
       rval, frame = videocapture.read() 
#       cv2.imwrite('pic.jpg', frame) 
       
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
@app.route('/video_feed') 
def video_feed(): 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 
if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=False, threaded=True) 
