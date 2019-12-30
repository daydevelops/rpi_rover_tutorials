from flask import Flask, Response
from flask import render_template
from flask_socketio import SocketIO, emit
from importlib import import_module
import os
import sys
import subprocess
import json

# import camera driver
sys.path.append('cam')
from camera_pi import Camera


app = Flask(__name__)

sys.path.append('robot')
import Robot as Robot

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

socketio = SocketIO(app,ping_timeout=3,ping_interval=1)

### Routes ###
@app.route('/')
def showController():
	return render_template('controller2.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

### SOCKET IO EVENTS ###

@socketio.on('connect')
def connect():
	print("client has connected")
	global robot
	print('Initializing Robot')
	robot = Robot.Robot()
	# start the camera
	# global cam
	# cam = subprocess.Popen('python3 /var/www/html/rpr2/cam/cam_feed.py',shell=True)

@socketio.on('disconnect')
def disconnect():
	print('Client disconnected')
	global robot
	# robot.stop()
	# global cam
	# cam.kill()

@socketio.on('speedInput')
def speedInput(data):
	global robot
	speeds = robot.drive(data)
	emit('speeds',json.dumps(speeds))

@socketio.on('updateTrim')
def updateTrim(change):
	global robot
	robot.changeTrim(change)

@socketio.on('camYaw')
def camYaw(input):
	global robot
	robot.yawCam(input)

if __name__ == "__main__":
	socketio.run(app,host="192.168.2.41")
