import concurrent.futures

import picarx_improved as pci
import rossros
from Sensor import Sensor
from Interpretation import Interpretation
from Controller import Controller

if __name__ == "__main__":
	# instantiating car object
	car = pci.Picarx()

	# instantiating sensor, interpret, and control objects
	sense = Sensor()
	interpreter = Interpretation()
	control = Controller(car)

	# creating busses
	senseBus = rossros.Bus(name='senseBus')
	interpBus = rossros.Bus(name='interpBus')
	controlBus = rossros.Bus(name='controlBus')
	timerBus = rossros.Bus(name='timeBus')
	termBus = rossros.Bus(name="termBus")

	# creating rossros nodes
	delay = 0.5
	timer = rossros.Timer(timerBus, delay=delay, termination_busses=termBus, name='timerP')

	# creating grayscale control objects
	gsSensorObj = rossros.Producer(sense.readData, senseBus, delay=delay, termination_busses=termBus, name='sensorP')
	gsInterpreterObj = rossros.ConsumerProducer(interpreter.getPosition, senseBus, interpBus, delay=delay,
											termination_busses=termBus, name='interpCP')
	gsControlObj = rossros.Consumer(control.control, interpBus, delay=delay, termination_busses=termBus, name='controlC')

	while (True):
		with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
			gsSensorThread = executor.submit(gsSensorObj)
			gsInterpThread = executor.submit(gsInterpreterObj)
			gsControlThread = executor.submit(gsControlObj)

		gsSensorThread.result()
		gsInterpThread.result()
		gsControlThread.result()
