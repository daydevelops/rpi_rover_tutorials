class MotorController(object):
	def __init__(self):
		print("starting serial connection")

	def stop(self):
		print("telling arduino to stop")

	def leftM(self, speed):
		print("telling Arduino to change left motor speed")

	def rightM(self, speed):
		print( "telling Arduino to change right motor speed")
