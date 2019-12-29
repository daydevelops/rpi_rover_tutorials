
import atexit
import MotorController as MC

class Robot(object):
	def __init__(self):
		self.left_trim = 0
		self.right_trim = 0
		# self.motors = MC.MotorController() #arduino motor controller class
		# Configure all motors to stop at program exit if desired.
		# atexit.register(self.stop)
		print("robot initialized")
		
	def changeTrim(self,change):
		self.left_trim += change['L']
		self.right_trim += change['R']

	def yawCam(self,input):
		# input will be in range of -1 to 1
		# convert to PWM range of 0 - 255
		pwm = (input/2) * 255
		# self.motors.yawCam(pwm)
		
	# def stop(self):
		# self.motors.stop()

	def drive(self,inputs):
		motorSpeeds = self.calculateMotorSpeeds(inputs)
		# self.leftM(motorSpeeds['LM'])
		# self.rightM(motorSpeeds['RM'])
		return motorSpeeds

	# def leftM(self, speed):
		# self.motors.rightM(speed)

	# def rightM(self, speed):
		# self.motors.leftM(speed)

	def calculateMotorSpeeds(self,data):
		# acceptable range of input data:
		#	y:[-1:1]
		#	x:[-1:1]
		#
		# acceptable range for motor commands:
		#	max defined by motor controller: [0:255]
		#	lets constrain that to: [0:200]

		# Left motor -> LM
		# Right motor -> RM
		RM = 100 * (data['surge'] - data['yaw'])
		LM = 100 * (data['surge'] + data['yaw'])
		# Filter out any really low motor speeds since they cant spin very slowly anyway
		threshhold = 20 # dont process motor speeds below this value
		
		# add or subtract the trim value to each motor
		if RM != 0:
			RM += abs(RM) * self.right_trim * (1 / RM)
		if LM != 0:
			LM += abs(LM) * self.left_trim * (1 / LM)

		if abs(RM) < threshhold:
			RM = 0
		if abs(LM) < threshhold:
			LM = 0

		return {'RM':RM,"LM":LM}
