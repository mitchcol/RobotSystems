import picarx_improved
import picarx_improved as pci
import Sensor
from Interpretation import *
from picarx_improved import *

class Controller():
	# constructor
	def __init__(self, scale=10):
		self._scale = scale

	# getters/setters
	@property
	def scale(self):
		return self._scale

	# member methods
	def control(self, px: pci.Picarx, position: float):
		# method to set the steering servo based on the input offset
		steeringAngle = -1 * self._scale * position
		px.set_dir_servo_angle(steeringAngle)
		return steeringAngle

if __name__ == '__main__':
	px = picarx_improved.Picarx()

	sensorObj = Sensor.Sensor()
	interObj = Interpretation(sensitivity=1, polarity=Polarity.DARK)
	contObj = Controller()

	while True:
		adcValues = sensorObj.readData()
		position = interObj.getPosition(adcValues)
		print(f'position: {position}')

		steeringAngle = contObj.control(px, position)
		print(f'steering angle: {steeringAngle}\n')

		time.sleep(2)
