from flask import Flask
from flask import render_template
from flask_socketio import SocketIO

app = Flask(__name__)

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
	# power up the robot

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
	# power down the robot

@socketio.on('speedInput')
def speedInput(data):
    print(data)

@socketio.on('updateTrim')
def updateTrim(change):
	print(change)

if __name__ == "__main__":
	socketio.run(app)
