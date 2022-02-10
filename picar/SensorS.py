import time
from ultrasonic import Ultrasonic
from pin import Pin

class Sensor():
	# constructor
	def __init__(self):
		# setting up ultrasonic readings
		self._trigPin = Pin("D2")
		self._echoPin = Pin("D3")
		self._sonar = Ultrasonic(self._trigPin, self._echoPin)

	# getters/setters

	# member methods
	def readData(self):
		return self._sonar.read()

if __name__ == '__main__':
	# creating sensor object
	sonar = Sensor()

	# printing sensor readings to the console
	while True:
		distance = sonar.readData()
		print(distance)
		time.sleep(0.5)