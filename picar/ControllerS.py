import time

import picarx_improved as pci
from InterpretationS import Interpretation
from InterpretationS import SonarMove
from SensorS import *

class Controller():
	# constructor
	def __init__(self, px: pci.Picarx):
		self._px = px

	# getters/setters

	# member methods
	def control(self, stopFlag: SonarMove):
		# method to set the steering servo based on the input offset
		if stopFlag == SonarMove.STOP:
			self._px.stop()
			return 1

		self._px.forward(30)
		return 0

if __name__ == '__main__':
	px = pci.Picarx()

	sensorObj = Sensor()
	interObj = Interpretation()
	contObj = Controller(px)

	while True:
		distance = sensorObj.readData()
		stopFlag = interObj.checkStop(distance)
		print(f'stopFlag: {stopFlag}')

		moveFlag = contObj.control(stopFlag)
		print(f'moveFlag: {moveFlag}\n')

		time.sleep(1)
