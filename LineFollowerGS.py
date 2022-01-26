import time
import sys

import picarx_improved as pci
from Controller import Controller
from Interpretation import Interpretation
from Interpretation import Polarity
from Sensor import Sensor

# creating car object
px = pci.Picarx()

# creating sensor, interpretation, and controller objects
sensorObj = Sensor()
interObj = Interpretation(sensitivity=1, polarity=Polarity.DARK)
contObj = Controller()

# setting up the loop from the input argument
if len(sys.argv) >= 2:
	runtime = float(sys.argv[1])
else:
	runtime = 10

timeout = time.time() + runtime

while True:
	px.forward(30)
	adcValues = sensorObj.readData()
	position = interObj.getPosition(adcValues)
	steeringAngle = contObj.control(px, position)

	if time.time() > timeout:
		break

px.stop()