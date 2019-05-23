
import atexit
import MotorController as MC

class Robot(object):
	def __init__(self):
		self.left_trim = 10
		self.right_trim = -10
		self.motors = MC.MotorController() #arduino motor controller class
		# Configure all motors to stop at program exit if desired.
		atexit.register(self.stop)
		print("robot initialized")
		
	def changeTrim(self,change):
		self.left_trim += change['L']
		self.right_trim += change['R']
		
	def stop(self):
		self.motors.stop()

	def drive(self,inputs):
		motorSpeeds = self.calculateMotorSpeeds(inputs)
		self.leftM(motorSpeeds['LM'])
		self.rightM(motorSpeeds['RM'])

	def leftM(self, speed):
		self.motors.rightM(speed)

	def rightM(self, speed):
		self.motors.leftM(speed)

	def calculateMotorSpeeds(self,data):
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
		
		# Apply trims to left and right motors
		if (RM > 0):
			RM += self.right_trim
		elif (RM < 0):
			RM -= self.right_trim
			
		if (LM > 0):
			LM += self.left_trim
		elif (LM < 0):
			LM -= self.left_trim
			
		
		return {'RM':RM,"LM":LM}
