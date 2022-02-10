import time

import picarx_improved as pci
from InterpretationGS import Interpretation
from InterpretationGS import Polarity
from SensorGS import Sensor
from Bus import Bus

class Controller():
	# constructor
	def __init__(self, px: pci.Picarx, scale=20):
		self._scale = scale
		self._px = px

	# getters/setters
	@property
	def scale(self):
		return self._scale

	# member methods
	def control(self, position: float):
		# method to set the steering servo based on the input offset
		steeringAngle = self._scale * position
		self._px.set_dir_servo_angle(steeringAngle)
		return steeringAngle

	def controlThread(self, interpretBus: Bus, controlBus: Bus, delay):
		while(True):
			# read from interpretBus
			position = interpretBus.message

			# write steering angle to controlBus
			controlBus.message(self.control(position))

			time.sleep(delay)

if __name__ == '__main__':
	px = pci.Picarx()

	sensorObj = Sensor()
	interObj = Interpretation(sensitivity=1, polarity=Polarity.DARK)
	contObj = Controller()

	while True:
		adcValues = sensorObj.readData()
		position = interObj.getPosition(adcValues)
		print(f'position: {position}')

		steeringAngle = contObj.control(px, position)
		print(f'steering angle: {steeringAngle}\n')

		time.sleep(2)
