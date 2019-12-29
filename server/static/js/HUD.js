var rover_heading; // compass data
var cam_heading; // compass data
var m1_speed = 0;
var m2_speed = 0;

function updateHUD() {
    console.log('m1: '+m1_speed);
	document.querySelector('#m1-pos-input').value = m1_speed;
    document.querySelector('#m2-pos-input').value = m2_speed;
    var cam_angle = cam_yaw * 100;
    document.querySelector("#cam-yaw-wrapper").style['transform'] = ('rotate('+cam_angle+'deg)');
    document.querySelector("#right-trim-val").innerHTML = trims['R'];
    document.querySelector("#left-trim-val").innerHTML = trims['L'];
}
