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
		adc_value_list = []
		adc_value_list.append(self.chn_0.read())
		adc_value_list.append(self.chn_1.read())
		adc_value_list.append(self.chn_2.read())
		return adc_value_list