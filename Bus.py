from readerwriterlock import rwlock

class Bus():
	# constructor
	def __init__(self):
		self._message = None
		self._lock = rwlock.RWLockWriteD()

	# getters/setters
	@property
	def message(self):
		with self._lock.gen_rlock():
			return self._message

	@message.setter
	def message(self, message):
		with self._lock.gen_wlock():
			self._message = message
