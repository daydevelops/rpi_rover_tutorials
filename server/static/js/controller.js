var socket;

function powerOff() {
	// switch to on button display
	$('#connected').css('display','none');
	$('#not-connected').css('display','block');

	closeSocket();
}

function powerOn() {
	// switch to controller display
	$('#not-connected').css('display','none');
	$('#connected').css('display','block');

	openSocket();
}

function openSocket() {
	// initialize socket
	socket = io.connect('http://' + document.domain + ':' + location.port);
	// event listener for when the connection to the server is established
	socket.on('connect', function() {
		console.log('We are connected!')
	});
}

function closeSocket() {
	// send disconnect msg to server
	socket.emit('disconnect');
	socket.disconnect();
	console.log('We have disconnected');
}

function updateMotorSpeeds() {
	data = {
		'speed':$('#speed-input').val(),
		'heading':$('#heading-input').val()
	}
	socket.emit('speedInput',data);
}

function changeTrim(data) {
	socket.emit('updateTrim',data);
}
