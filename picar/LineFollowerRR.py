import concurrent.futures

import picarx_improved as pci
import rossros

import SensorGS as gss
import InterpretationGS as gsi
import ControllerGS as gsc

import SensorS as ss
import InterpretationS as si
import ControllerS as sc

if __name__ == "__main__":
	# instantiating car object
	px = pci.Picarx()

	# instantiating sensor, interpret, and control objects for gray scale and sonar
	gsSense = gss.Sensor()
	gsInterp = gsi.Interpretation()
	gsControl = gsc.Controller(px)

	sSense = ss.Sensor()
	sInterp = si.Interpretation()
	sControl = sc.Controller(px)

	# creating busses
	gsSenseBus = rossros.Bus(name='gsSenseBus')
	gsInterpBus = rossros.Bus(name='gsInterpBus')
	gsControlBus = rossros.Bus(name='gsControlBus')

	sSenseBus = rossros.Bus(name='sSenseBus')
	sInterpBus = rossros.Bus(name='sInterpBus')
	sControlBus = rossros.Bus(name='sControlBus')

	timerBus = rossros.Bus(name='timeBus')
	termBus = rossros.Bus(name="termBus")

	# creating rossros nodes
	delay = 0.5
	timer = rossros.Timer(timerBus, delay=delay, termination_busses=termBus, name='timerP')

	# creating grayscale control objects
	gsSensorObj = rossros.Producer(gsSense.readData, gsSenseBus, delay=delay, termination_busses=termBus,
								   name='gsSensorP')
	gsInterpreterObj = rossros.ConsumerProducer(gsInterp.getPosition, gsSenseBus, gsInterpBus, delay=delay,
												termination_busses=termBus, name='gsInterpCP')
	gsControlObj = rossros.Consumer(gsControl.control, gsInterpBus, delay=delay, termination_busses=termBus,
									name='gsControlC')

	# creating sonar control objects
	sSensorObj = rossros.Producer(sSense.readData, sSenseBus, delay=delay, termination_busses=termBus, name='sSensorP')
	sInterpObj = rossros.ConsumerProducer(sInterp.checkStop, sSenseBus, sInterpBus, delay=delay,
										  termination_busses=termBus, name='sInterpCP')
	sControlObj = rossros.Consumer(sControl.control, sInterpBus, delay=delay, termination_busses=termBus,
								   name='sControlC')

	while (True):
		with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
			# timer thread
			timerThread = executor.submit(timer)

			# gray scale threads
			gsSensorThread = executor.submit(gsSensorObj)
			gsInterpThread = executor.submit(gsInterpreterObj)
			gsControlThread = executor.submit(gsControlObj)

			# sonar threads
			sSensorThread = executor.submit(sSensorObj)
			sInterpThread = executor.submit(sInterpObj)
			sControlThread = executor.submit(sControlObj)

		# results
		timerThread.result()

		gsSensorThread.result()
		gsInterpThread.result()
		gsControlThread.result()

		sSensorThread.result()
		sInterpThread.result()
		sControlThread.result()
