import time
from enum import Enum
import SensorGS

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
	def getPosition(self, adcValueList: list):
		# using the input values to determine where the picar is relative to the line

		# clamping the values to the min and max bounds provided in the documentation
		s0, s1, s2 = self.clampADCValues(adcValueList)

		# bit of a slick conceptual equation here that Abhinav and I discussed. We subtract the two outer values to
		# determine if we are pointed to the left or right then, we divide by the center sensor to normalize the
		# value between -1 and 1. The higher the center value the smaller position will be, the smaller the
		# center value, the higher the turn will be
		pos = ((s2 - s0) / s1) * self._sensitivity

		# checking if we have light polarity.
		if self._polarity == Polarity.LIGHT:
			# in this case, we should be able to just flip the sign
			pos = -1 * pos

		return pos

	def clampADCValues(self, adcValueList: list):
		# clamps the adc values in the list to values between 900 (black) and 1500 (white)
		# reduced the min value so we dont have issues normalizing the values later.
		minValue = 750
		maxValue = 1500

		if adcValueList[0] < minValue:
			s0 = minValue
		elif adcValueList[0] > maxValue:
			s0 = maxValue
		else:
			s0 = adcValueList[0]

		if adcValueList[1] < minValue:
			s1 = minValue
		elif adcValueList[1] > maxValue:
			s1 = maxValue
		else:
			s1 = adcValueList[1]

		if adcValueList[2] < minValue:
			s2 = minValue
		elif adcValueList[2] > maxValue:
			s2 = maxValue
		else:
			s2 = adcValueList[2]

		return s0, s1, s2

	def normalizeValue(self, value, min, max):
		# normalizes the input value according to the provided min and max args
		return (value - min) / (max - min)

	def interpretThread(self, senseBus, interpretBus, delay):
		while (True):
			# get data from senseBus
			adcValues = senseBus.message
			# store data in interpret bus message
			interpretBus.message(self.getPosition(adcValues))

			time.sleep(delay)


if __name__ == "__main__":
	sensorObj = SensorGS.Sensor()
	interObj = Interpretation(sensitivity=1, polarity=Polarity.DARK)

	while True:
		adcValues =  sensorObj.readData()
		print(f'adc values: {adcValues}')

		position = interObj.getPosition(adcValues)
		print(f'position: {position}\n')

		time.sleep(1)

