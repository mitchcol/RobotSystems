class Servo(object):
	MAX_PW = 2500
	MIN_PW = 500
	_freq = 50

	def __init__(self, pwm):
		super().__init__()

	def map(self, x, in_min, in_max, out_min, out_max):
		return 1

	# angle ranges -90 to 90 degrees
	def angle(self, angle):
		pass
