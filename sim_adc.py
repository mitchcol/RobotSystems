class ADC():
	ADDR = 0x14  # 扩展板的地址为0x14

	def __init__(self, chn):
		super().__init__()

	def read(self):
		return 1

	def read_voltage(self):  # 将读取的数据转化为电压值（0~3.3V）
		return 1

def test():
	import time
	adc = ADC(0)
	while True:
		print(adc.read())
		time.sleep(1)


if __name__ == '__main__':
	test()