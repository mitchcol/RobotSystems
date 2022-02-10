
timer = [{"arr": 0}] * 4

class PWM:
	REG_CHN = 0x20
	REG_FRE = 0x30
	REG_PSC = 0x40
	REG_ARR = 0x44

	ADDR = 0x14

	CLOCK = 72000000

	def __init__(self, channel, debug="critical"):
		pass

	def i2c_write(self, reg, value):
		pass

	def freq(self, *freq):
		pass

	def prescaler(self, *prescaler):
		return 1

	def period(self, *arr):
		return 1

	def pulse_width(self, *pulse_width):
		return 1

	def pulse_width_percent(self, *pulse_width_percent):
		return 1
