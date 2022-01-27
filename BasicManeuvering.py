import time
import cv2

import picarx_improved as pci
from Controller import Controller
from Interpretation import Interpretation
from Interpretation import Polarity
from Sensor import Sensor
from Camera	import Camera

# note! all these functions take a list as their argument. any argument checking is done
# inside the function body. Remember, the first element in the list is the function name.

# using class structure here since it'll be easier than passing the picar object and checking
# type each use.
class BasicManeuvering():
	# constructor
	def __init__(self):
		# creating picar object
		self.px = pci.Picarx()

		# loading dictionary with callable functions. acts like a switch
		self.switch = dict()
		self.switch['forward'] = self.forward
		self.switch['backward'] = self.backward
		self.switch['parallelPark'] = self.parallelPark
		self.switch['kTurn'] = self.kTurn
		self.switch['lineFollower'] = self.lineFollower
		self.switch['cameraFollower'] = self.cameraFollower
		self.switch['reset'] = self.reset
		self.switch['debugTest'] = self.test

	# member methods
	def checkArgs(self, args: list, numArgs):
		# just checks that the list has the correct number of arguments
		# remember that the function is still in the list of passed arguments
		if len(args) == (numArgs+1):
			return True
		else:
			return False

	def forward(self, args: list):
		# forward(speed, angle, time)

		# checking arguments
		numArgs = 3
		if not self.checkArgs(args, numArgs):
			raise UserWarning

		# unpacking arg list
		speed = float(args[1])
		angle = float(args[2])
		driveTime = float(args[3])

		# setting angle
		self.px.set_dir_servo_angle(angle)

		# moving forward
		self.px.forward(speed)
		time.sleep(driveTime)
		self.px.stop()

	def backward(self, args: list):
		# backward(speed, angle, time)

		# checking arguments
		numArgs = 3
		if not self.checkArgs(args, numArgs):
			raise UserWarning

		# unpacking arg list
		speed = float(args[1])
		angle = float(args[2])
		driveTime = float(args[3])

		# setting angle
		self.px.set_dir_servo_angle(angle)

		# moving backward
		self.px.backward(speed)
		time.sleep(driveTime)
		self.px.stop()

	def parallelPark(self, args: list):
		# parallelPark(speed, dir)

		# checking arguments
		numArgs = 2
		if not self.checkArgs(args, numArgs):
			raise UserWarning

		# unpacking arg list
		speed = float(args[1])
		parkDir = args[2]

		if parkDir == 'left':
			turnCoeff = -1
		else:
			turnCoeff = 1

		# move forward
		self.px.forward(speed)
		time.sleep(1)
		self.px.stop()

		# angle wheels into curb and move backwards
		turnAng1 = 30
		self.px.set_dir_servo_angle(turnAng1 * turnCoeff)
		# move back
		self.px.backward(speed)
		time.sleep(1)
		self.px.stop()

		# reset dir servo angle and back up straight
		self.px.set_dir_servo_angle(0)
		# back up
		self.px.backward(speed)
		time.sleep(1)
		self.px.stop()

		# angle wheels into street and back up
		turnAng2 = 25
		self.px.set_dir_servo_angle(turnAng2 * -turnCoeff)
		# move backward
		self.px.backward(speed)
		time.sleep(1)
		self.px.stop()

		# straighten wheels and move forward to correct
		self.px.set_dir_servo_angle(0)
		# move forward
		self.px.forward(speed)
		time.sleep(0.5)
		self.px.stop()

	def kTurn(self, args: list):
		# kTurn(speed, dir)
		# checking arguments
		numArgs = 2
		if not self.checkArgs(args, numArgs):
			raise UserWarning

		# unpacking arg list
		speed = float(args[1])
		turnDir = args[2]

		if turnDir == 'left':
			turnCoeff = -1
		else:
			turnCoeff = 1

		turnAng = 30

		# turn 1
		self.px.set_dir_servo_angle(turnAng * turnCoeff)
		# move forward
		self.px.forward(speed)
		time.sleep(1)
		self.px.stop()

		# move forward
		self.px.set_dir_servo_angle(0)
		self.px.forward(speed)
		time.sleep(0.75)
		self.px.stop()

		# turn 2
		self.px.set_dir_servo_angle(-turnAng * turnCoeff)
		# move backward
		self.px.backward(speed)
		time.sleep(1)
		self.px.stop()

		# turn 1
		self.px.set_dir_servo_angle(turnAng * turnCoeff)
		# move forward
		self.px.forward(speed)
		time.sleep(1.8)
		self.px.stop()

		self.px.set_dir_servo_angle(0)

	def lineFollower(self, args: list):
		# lineFollower(speed, scale, time)

		# checking arguments
		numArgs = 3
		if not self.checkArgs(args, numArgs):
			raise UserWarning

		# unpacking argument list
		speed = int(args[1])
		scale = float(args[2])
		runtime = int(args[3])

		# creating sensor, interpretation, and controller objects
		sensorObj = Sensor()
		interObj = Interpretation(sensitivity=1)
		contObj = Controller(scale=scale)

		# setting up the loop from the input argument
		timeout = time.time() + runtime

		while True:
			self.px.forward(speed)
			adcValues = sensorObj.readData()
			position = interObj.getPosition(adcValues)
			contObj.control(self.px, position)

			if time.time() > timeout:
				break

		self.px.stop()

	def cameraFollower(self, args: list):
		# lineFollower(speed)

		# checking arguments
		numArgs = 1
		if not self.checkArgs(args, numArgs):
			raise UserWarning

		# unpacking argument list
		speed = int(args[1])

		camera = Camera()
		for frame in camera.camera.capture_continuous(camera.rawCapture, format='bgr', use_video_port=True):
			self.px.forward(speed)

			frameArry = frame.array

			laneLines = camera.detectLane(frameArry)
			linesImg = camera.displayLaneLines(frameArry, laneLines)
			cv2.imshow('lines', linesImg)

			steeringAngle = camera.getSteeringAngle(frameArry, laneLines)
			hardingImg = camera.displayHeadingLine(frameArry, steeringAngle)
			cv2.imshow('heading', hardingImg)

			self.px.set_dir_servo_angle(steeringAngle)

			camera.rawCapture.truncate(0)

			key = cv2.waitKey(1) & 0xFF
			if key == 27:
				camera.camera.close()
				self.px.stop()
				break

	def reset(self, args: list):
		# just resets the drive servo to 0
		# no arguments required
		self.px.set_dir_servo_angle(0)

	def test(self, args: list):
		print(args)

if __name__ == '__main__':
	# creating basic maneuvering object
	bmObj = BasicManeuvering()

	# printing help menu
	print('Please enter one of the commands below (comma separated):')
	print('\t- forward(speed, angle, time)')
	print('\t- backward(speed, angle, time)')
	print('\t- parallelPark(speed, dir)')
	print('\t- kTurn(speed, dir)')
	print('\t- lineFollower(speed, scale, time)')
	print('\t- cameraFollower(speed)')
	print('\t- reset <--- zeros all servos')
	print('\t- * <--- issues the previous command')
	print('\t- exit <--- terminates the program')
	print('\n\tUsage: function,arg1,arg2,arg3,...')
	print('************************************************************************')

	# starting endless loop so the user can keep entering commands
	done = False
	first = True
	while not done:
		# prompting the user to input a command
		inputStr = input('@ ')

		if inputStr == '*':
			if first:
				print('\tNeed to enter a command before using *.')
				continue
			else:
				inputStr = prevInputStr

		inputList = inputStr.split(',')

		if inputList[0] == 'exit':
			print('Exit...')
			done = True
		else:
			try:
				bmObj.switch[inputList[0]](inputList)
				prevInputStr = inputStr

				if first:
					first = False
			except KeyError:
				# function doesn't exist
				print('\tCommand not found. Please verify with the list above.')
				print('\tUsage: function,arg1,arg2,arg3,...')
			except UserWarning:
				print('\tToo few or too many arguments. Please verify with the list above.')
				print('\tUsage: function,arg1,arg2,arg3,...')

