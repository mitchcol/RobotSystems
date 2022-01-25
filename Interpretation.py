from enum import Enum
import Sensor

class Polarity(Enum):
	DARK = 0
	LIGHT = 1

class Interpretation():
	# constructor
	def __init__(self, sensitivity=1, polarity=Polarity.DARK):
		self._sensitivity = sensitivity
		self._polarity = polarity

	# getters/setters
	@property
	def sensitivity(self):
		return self._sensitivity

	@property
	def polarity(self):
		return self._polarity

	# member methods
	def getPosition(self, adcValueList: list):
		# using the input values to determine where the picar is relative to the line

		# clamping the values to the min and max bounds provided in the documentation
		s0, s1, s2 = self.clampADCValues(adcValueList)

		# normalizing the current values
		s0Norm = self.normalizeValue(s0, 900, 1500)
		s1Norm = self.normalizeValue(s1, 900, 1500)
		s2Norm = self.normalizeValue(s2, 900, 1500)

		# inverting the norm if
		if self._polarity.LIGHT:
			s0Norm = 1 - s0Norm
			s1Norm = 1 - s1Norm
			s2Norm = 1 - s2Norm

		# bit of a slick conceptual equation here that Abhinav told me about. After we normalize the values
		# between 0 and 1, we subtract the two outer values to determine if we are pointed to the left or right
		# then, we divide by the center sensor to normalize the value between -1 and 1. The higher the center value
		# the smaller position will be, the smaller the center value, the higher the turn will be
		try:
			pos = (s2Norm - s0Norm) / s1Norm
		except ZeroDivisionError:
			# if the s1 value is 0, then the middle sensor isn't on the line at all
			if s2Norm >= s0Norm:
				pos = s2Norm
			else:
				pos = s0Norm

		return pos

	def clampADCValues(self, adcValueList: list):
		# clamps the adc values in the list to values between 900 (black) and 1500 (white)
		minValue = 900
		maxValue = 1500

		if adcValueList[0] < 900:
			s0 = minValue
		elif adcValueList[0] > 1500:
			s0 = maxValue
		else:
			s0 = adcValueList[0]

		if adcValueList[1] < 900:
			s1 = minValue
		elif adcValueList[1] > 1500:
			s1 = maxValue
		else:
			s1 = adcValueList[1]

		if adcValueList[2] < 900:
			s2 = minValue
		elif adcValueList[2] > 1500:
			s2 = maxValue
		else:
			s2 = adcValueList[2]

		return s0, s1, s2

	def normalizeValue(self, value, min, max):
		# normalizes the input value according to the provided min and max args
		return (value - min) / (max - min)

if __name__ == "__main__":
	sensorObj = Sensor.Sensor()
	interObj = Interpretation()

	while True:
		adcValues =  sensorObj.readData()
		print(f'adc values: {adcValues}')

		position = interObj.getPosition(adcValues)
		print(f'position: {position}\n')

