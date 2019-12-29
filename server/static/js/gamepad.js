var haveEvents = 'ongamepadconnected' in window;
var controller_check_interval;
var controller_old;
var controller;
var button_handlers = {
  0:decrementLeftTrim,  // a
  1:decrementRightTrim,  // b
  2:incrementLeftTrim,  // x
  3:incrementRightTrim,  // y
  4:pressedButton,  // lb
  5:pressedButton,  // rb
  6:driveBackward,  // lt
  7:driveForward,  // rt
  8:powerOff,  // sel
  9:powerOn,  // start
  10:pressedButton, // ls
  11:pressedButton, // rs
  12:pressedButton, // du
  13:pressedButton, // dl
  14:pressedButton, // dr
  15:pressedButton  // dd
}
var axis_handlers = {
  0:yawRover, // lh
  1:joyMoved, // lv
  2:yawCamera, // rh
  3:pitchCamera, // rv
}

function pressedButton() {

}

function joyMoved() {

}

function connecthandler(e) {
  addgamepad(e.gamepad);
}

function addgamepad(gamepad) {
  console.log("adding gamepad")
  controller = gamepad;
  controller_check_interval = setInterval(updateStatus, 100);
}

function disconnecthandler(e) {
  removegamepad(e.gamepad);
}

function removegamepad(gamepad) {
  console.log("removing gamepad")
  controller = null;
  clearInterval(controller_check_interval);
  powerOff();
}

function updateStatus() {
  if (!haveEvents) {
    scangamepads();
  }
  for (i = 0; i < controller.buttons.length; i++) {
    var butt_old = controller_old.buttons[i];
    var butt = controller.buttons[i];
    
    if (i==6 || i==7) { // triggers, treat them as joy sticks
      if (butt.value>0.2) {
        button_handlers[i](butt.value);
      } else {
        button_handlers[i](0);
      }
    } else if (butt.pressed && !butt_old.pressed) {
      button_handlers[i](butt.value);
    }
  }

  for (i = 0; i < controller.axes.length; i++) {
    var joy = controller.axes[i];

    if (Math.abs(joy.toFixed(4))<0.2) {
      axis_handlers[i](0);
    } else {
      axis_handlers[i](joy.toFixed(4));
    }
  }

  updateHUD();
}

function scangamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  for (var i = 0; i < gamepads.length; i++) {
    if (gamepads[i]) {
      if (controller == null) {
        addgamepad(gamepads[i]);
      } else {
        controller_old = controller;
        controller = gamepads[i];
      }
    }
  }
}


window.addEventListener("gamepadconnected", connecthandler);
window.addEventListener("gamepaddisconnected", disconnecthandler);

if (!haveEvents) {
  setInterval(scangamepads, 500);
}

