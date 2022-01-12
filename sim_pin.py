class Pin(object):
	_dict = {
		"BOARD_TYPE": 12,
	}

	_dict_1 = {
		"D0": 17,
		"D1": 18,
		"D2": 27,
		"D3": 22,
		"D4": 23,
		"D5": 24,
		"D6": 25,
		"D7": 4,
		"D8": 5,
		"D9": 6,
		"D10": 12,
		"D11": 13,
		"D12": 19,
		"D13": 16,
		"D14": 26,
		"D15": 20,
		"D16": 21,
		"SW": 19,
		"LED": 26,
		"BOARD_TYPE": 12,
		"RST": 16,
		"BLEINT": 13,
		"BLERST": 20,
		"MCURST": 21,
	}

	_dict_2 = {
		"D0": 17,
		"D1": 4,  # Changed
		"D2": 27,
		"D3": 22,
		"D4": 23,
		"D5": 24,
		"D6": 25,  # Removed
		"D7": 4,  # Removed
		"D8": 5,  # Removed
		"D9": 6,
		"D10": 12,
		"D11": 13,
		"D12": 19,
		"D13": 16,
		"D14": 26,
		"D15": 20,
		"D16": 21,
		"SW": 25,  # Changed
		"LED": 26,
		"BOARD_TYPE": 12,
		"RST": 16,
		"BLEINT": 13,
		"BLERST": 20,
		"MCURST": 5,  # Changed
	}

	def __init__(self, *value):
		super().__init__()

	def check_board_type(self):
		pass

	def init(self, mode, pull=None):
		pass

	def dict(self, *_dict):
		pass

	def __call__(self, value):
		return self.value(value)

	def value(self, *value):
		return 1

	def on(self):
		return self.value(1)

	def off(self):
		return self.value(0)

	def high(self):
		return self.on()

	def low(self):
		return self.off()

	def mode(self, *value):
		return 1

	def pull(self, *value):
		return 1

	def irq(self, handler=None, trigger=None, bouncetime=200):
		pass

	def name(self):
		return 'name'

	def names(self):
		return [self.name, 'board name']

	class cpu(object):
		GPIO17 = 17
		GPIO18 = 18
		GPIO27 = 27
		GPIO22 = 22
		GPIO23 = 23
		GPIO24 = 24
		GPIO25 = 25
		GPIO26 = 26
		GPIO4 = 4
		GPIO5 = 5
		GPIO6 = 6
		GPIO12 = 12
		GPIO13 = 13
		GPIO19 = 19
		GPIO16 = 16
		GPIO26 = 26
		GPIO20 = 20
		GPIO21 = 21

		def __init__(self):
			pass

if __name__ == "__main__":
	import time

	mcu_reset = Pin("MCURST")
	mcu_reset.off()
	time.sleep(0.001)
	mcu_reset.on()
	time.sleep(0.01)