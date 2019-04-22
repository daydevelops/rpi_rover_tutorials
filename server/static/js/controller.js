
function powerOff() {
	// switch to on button display
	$('#connected').css('display','none');
	$('#not-connected').css('display','block');
}

function powerOn() {
	// switch to controller display
	$('#not-connected').css('display','none');
	$('#connected').css('display','block');
}

function updateMotorSpeeds() {
	console.log('speed: '+$("#speed-input").val()+'    heading: '+$("#heading-input").val())
}

function changeTrim(data) {
	console.log('updating Trim: Left->'+data.L+'    Right->'+data.R);
}
