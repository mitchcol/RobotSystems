import time
from enum import Enum
import SensorS

class SonarDist(Enum):
	CLOSE = 0
	MID = 1
	FAR = 2

class SonarMove(Enum):
	GO = 0
	STOP = 1

class Interpretation():
	# constructor
	def __init__(self, stopDist=SonarDist.MID):
		# setting the sonar stop dist
		if isinstance(stopDist, SonarDist):
			self._stopDist = stopDist
		else:
			# if it isn't then we set the normal default
			self._stopDist = SonarDist.MID

	# getters/setters
	@property
	def stopDist(self):
		return self._stopDist

	# member methods
	def checkStop(self, distance: float):
		# using the sonar distance to determine if we need to stop or not
		if (distance >= self._stopDist.value) or (distance < 0):
			return SonarMove.STOP

		return SonarMove.GO

if __name__ == "__main__":
	sensorObj = SensorS.Sensor()
	interObj = Interpretation()

	while True:
		distance =  sensorObj.readData()
		print(f'distance: {distance}')

		option = interObj.checkStop(distance)
		print(f'option: {option}\n')

		time.sleep(1)

