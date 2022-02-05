import time

from adc import ADC

class Sensor():
	# constructor
	def __init__(self):
		self.chn_6 = ADC("A6")
		self.chn_7 = ADC("A7")

	# getters/setters

	# member methods
	def readData(self):
		adcValueList = []
		adcValueList.append(self.chn_6.read())
		adcValueList.append(self.chn_7.read())

		return adcValueList


if __name__ == '__main__':
	# creating sensor object
	sonar = Sensor()

	while True:
		adcValueList = sonar.readData()

		print(adcValueList)