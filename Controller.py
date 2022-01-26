import picarx_improved as pci

class Controller():
	# constructor
	def __init__(self, scale=10):
		self._scale = scale

	# getters/setters
	@property
	def scale(self):
		return self._scale

	# member methods
	def control(self, px: pci.Picarx, position: float):
		# method to set the steering servo based on the input offset
		steeringAngle = -1 * self._scale * position
		px.set_dir_servo_angle(steeringAngle)
		return steeringAngle


