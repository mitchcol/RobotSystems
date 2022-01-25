

class Controller():
	# constructor
	def __init__(self, offset):
		self._offset = offset

	# getters/setters
	@property
	def offset(self):
		return self._offset

	# member methods
	def control(self):
