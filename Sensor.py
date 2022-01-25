from adc import ADC

class Sensor():
	# constructor
	def __init__(self):
		self.chn_0 = ADC("A0")
		self.chn_1 = ADC("A1")
		self.chn_2 = ADC("A2")

	# getters/setters

	# member methods
	def readData(self):
		adcValueList = []
		adcValueList.append(self.chn_0.read())
		adcValueList.append(self.chn_1.read())
		adcValueList.append(self.chn_2.read())
		return adcValueList