import picarx_improved as pi

# note! all these functions take a list as their argument. any argument checking is done
# inside the function body. Remember, the first element in the list is the function name.

def forward(args: list):
	# forward(speed, angle)
	return

def backward(args: list):
	# backward(speed, angle)
	return

def parallelPark(args: list):
	# parallelPark(speed, dir)
	return

def kTurn(args: list):
	# kTurn(speed, initAng, dir)
	return

# loading dictionary with callable functions. acts like a switch
switch = dict()
switch['forward'] = forward
switch['backward'] = backward
switch['parallelPark'] = parallelPark
switch['kTurn'] = kTurn

if __name__ == '__main__':
	# printing help menu
	print('Please enter one of the commands below (comma separated):')
	print('\t- forward(speed, angle)')
	print('\t- backward(speed, angle)')
	print('\t- parallelPark(speed, angle)')
	print('\t- kTurn(speed, initAng, dir)')
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
				switch[inputList[0]](inputList)
				print(inputList)
			except KeyError:
				# function doesn't exist
				print('\tPlease verify that your command is in the list.')
				print('\tUsage: function,arg1,arg2,arg3,...')

