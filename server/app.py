from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
import sys

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
	return render_template('controller.html')


### SOCKET IO EVENTS ###

@socketio.on('connect')
def connect():
	print("client has connected")
	global robot
	print('Initializing Robot')
	robot = Robot.Robot()

@socketio.on('disconnect')
def disconnect():
	print('Client disconnected')
	global robot
	robot.stop()

@socketio.on('speedInput')
def speedInput(data):
	global robot
	robot.drive(data)

@socketio.on('updateTrim')
def updateTrim(change):
	print(change)

if __name__ == "__main__":
	socketio.run(app)
