import picarx_improved as pi
import time

# note! all these functions take a list as their argument. any argument checking is done
# inside the function body. Remember, the first element in the list is the function name.

# using class structure here since it'll be easier than passing the picar object and checking
# type each use.
class BasicManeuvering():
	# constructor
	def __init__(self):
		# creating picar object
		self.px = pi.Picarx()

		# loading dictionary with callable functions. acts like a switch
		self.switch = dict()
		self.switch['forward'] = self.forward
		self.switch['backward'] = self.backward
		self.switch['parallelPark'] = self.parallelPark
		self.switch['kTurn'] = self.kTurn

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
		return

	def kTurn(self, args: list):
		# kTurn(speed, initAng, dir)
		return

	def reset(self):
		# just resets the drive servo to 0
		# no arguments
		self.px.set_dir_servo_angle(0)

if __name__ == '__main__':
	# creating basic maneuvering object
	bmObj = BasicManeuvering()

	# printing help menu
	print('Please enter one of the commands below (comma separated):')
	print('\t- forward(speed, angle, time)')
	print('\t- backward(speed, angle, time)')
	print('\t- parallelPark(speed, angle)')
	print('\t- kTurn(speed, initAng, dir)')
	print('\t- reset <--- zeros all servos')
	print('\t- exit <--- terminates the program')
	print('\n\tUsage: function,arg1,arg2,arg3,...')
	print('************************************************************************')

	# starting endless loop so the user can keep entering commands
	done = False
	while not done:
		# prompting the user to input a command
		inputStr = input('@ ')

		# separating the function from the arguments
		inputList = inputStr.split(',')

		if inputList[0] == 'exit':
			print('Exit...')
			done = True
		else:
			try:
				bmObj.switch[inputList[0]](inputList)
			except KeyError:
				# function doesn't exist
				print('\tCommand not found. Please verify with the list above.')
				print('\tUsage: function,arg1,arg2,arg3,...')
			except UserWarning:
				print('\tToo few or too many arguments. Please verify with the list above.')
				print('\tUsage: function,arg1,arg2,arg3,...')

