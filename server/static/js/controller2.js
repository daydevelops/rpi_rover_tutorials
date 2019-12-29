var socket;
var is_powered_on = false; // is the controller on or off
var rover_surge = 0;
var rover_yaw = 0;
var cam_yaw = 0;
var cam_pitch = 0;
var trims = {L:0,R:0};
var motor_update_interval;

function powerOff() {
	if (is_powered_on) {
		// switch to on button display
		$('#connected').css('display', 'none');
		$('#not-connected').css('display', 'block');
		is_powered_on = false;
		closeSocket();
		clearInterval(motor_update_interval);
	}
}

function powerOn() {
	if (!is_powered_on) {
		// switch to controller display
		$('#not-connected').css('display', 'none');
		$('#connected').css('display', 'block');
		is_powered_on = true;
		openSocket();
		motor_update_interval = setInterval(sendMotorSpeeds,100);
	}
}

function openSocket() {
	// initialize socket
	socket = io.connect('http://' + document.domain + ':' + location.port);
	// event listener for when the connection to the server is established
	socket.on('connect', function () {
		console.log('We are connected!')
	});

	socket.on('speeds', function(speeds) {
		speeds = JSON.parse(speeds);
		m1_speed = speeds['LM'];
		m2_speed = speeds['RM'];
	})
}

function closeSocket() {
	// send disconnect msg to server
	socket.emit('disconnect');
	socket.disconnect();
	console.log('We have disconnected');
}

function sendMotorSpeeds() {
	if (!is_powered_on) return false;
	data = {
		'surge': rover_surge,
		'yaw': rover_yaw
	}
	// console.log('updating speed: '+rover_surge);
	// console.log('updating heading: '+rover_yaw);
	socket.emit('speedInput', data);
}

function yawCamera(value) {
	if (!is_powered_on) return false;
	if (Math.abs(value) < 0.15) {
		value = 0;
	}
	if ((value == 0 && cam_yaw != 0) || Math.abs(value-cam_yaw)>0.05) {
		// console.log('yawing cam to '+value);
		socket.emit('camYaw', value);
	}
	cam_yaw = value;
}

function pitchCamera(value) {
	if (!is_powered_on) {
		return false;
	}
	if (Math.abs(value) < 0.15) {
		value = 0;
	}
	if ((value == 0 && cam_pitch != 0) || Math.abs(value-cam_pitch)>0.05) {
		// console.log('pitching cam to '+value);
		// socket.emit('camPitch', value);
	}
	cam_pitch = value;
}

function yawRover(value) {
	if (!is_powered_on) return false;
	rover_yaw = 1*value;
}

function driveForward(value) {
	if (!is_powered_on) return false;
	// gets called after driveBackward, and sends a default value of zero
	// when the trigger is unpressed, which would overwrite the value set in 
	// driveBackward(), so check for this condition.
	if (value==0 && rover_surge < 0) {
		//do nothing
	} else {
		rover_surge = value;
	}
}

function driveBackward(value) {
	if (!is_powered_on) return false;
	rover_surge = -1*value;
}

function incrementLeftTrim() {
	if (!is_powered_on) return false;
	console.log('changing trim');
	trims['L']++;
	socket.emit('updateTrim', {
		L:1,
		R:0
	});
}

function incrementRightTrim() {
	if (!is_powered_on) return false;
	console.log('changing trim');
	trims['R']++;
	socket.emit('updateTrim', {
		L:0,
		R:1
	});
}

function decrementLeftTrim() {
	if (!is_powered_on) return false;
	console.log('changing trim');
	trims['L']--;
	socket.emit('updateTrim', {
		L:-1,
		R:0
	});
}

function decrementRightTrim() {
	if (!is_powered_on) return false;
	console.log('changing trim');
	trims['R']--;
	socket.emit('updateTrim', {
		L:0,
		R:-1
	});
}

