import time

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

while True:
	px.forward(30)
	adcValues = sensorObj.readData()
	position = interObj.getPosition(adcValues)
	steeringAngle = contObj.control(px, position)