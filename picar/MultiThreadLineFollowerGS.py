import concurrent.futures

import picarx_improved as pci
from SensorGS import Sensor
from InterpretationGS import Interpretation
from ControllerGS import Controller
from Bus import Bus

if __name__ == "__main__":
	car = pci.Picarx()

	senseBus = Bus()
	interpretBus = Bus()
	controlBus = Bus()

	sense = Sensor()
	interpreter = Interpretation()
	control = Controller(car)

	delay = 0.5
	while(True):
		with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
			eSensor = executor.submit(sense.senseThread, senseBus, delay)
			eInterpreter = executor.submit(interpreter.interpretThread, senseBus, interpretBus, delay)
			eController = executor.submit(control.controlThread, interpretBus, controlBus, delay)

		eSensor.result()
		eInterpreter.result()
		eController.result()

