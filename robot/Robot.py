
import atexit
import MotorController as MC

class Robot(object):
	def __init__(self):
		self._left_trim = 0
		self._right_trim = 0
		self.motors = MC.MotorController() #arduino motor controller class
		# Configure all motors to stop at program exit if desired.
		atexit.register(self.stop)
		print("robot initialized")

	def stop(self):
		self.motors.stop()

	def drive(self,inputs):
		motorSpeeds = self.processMotorInputs(inputs)
		self.leftM(int(motorSpeeds['LM']))
		self.rightM(int(motorSpeeds['RM']))

	def leftM(self, speed):
		self.motors.rightM(speed)

	def rightM(self, speed):
		self.motors.leftM(speed)

	def processMotorInputs(self,data):
		# acceptable range of input data:
		#	y:[-100:100]
		#	x:[-100:100]
		#
		# acceptable range for motor commands:
		#	max defined by motor controller: [0:255]
		#	lets constrain that to: [0:200]

		# Left motor -> LM
		# Right motor -> RM
		RM = int(data['speed']) - int(data['heading'])
		LM = int(data['speed']) + int(data['heading'])

		return {'RM':RM,"LM":LM}
