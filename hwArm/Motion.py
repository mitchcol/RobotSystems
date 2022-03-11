import sys
import cv2
import time
import Camera
from math import sqrt
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *


class Motion:
	def __init__(self) -> None:
		# servo position val
		self.servo1 = 500

		# IK solver and motion planner/exector
		self.arm = ArmIK()

		# Arm statuses
		self.is_moving = False
		self.grasping = False
		self.executing = False
		self.current_block = 0
		self.stack_height = 0

		# Placement positions
		self.quick_place_coords = {
			'red': (-15 + 0.5, 12 - 0.5, 1.5),
			'green': (-15 + 0.5, 6 - 0.5, 1.5),
			'blue': (-15 + 0.5, 0 - 0.5, 1.5),
		}

	def stack(self, blocks, stack_pose=(0, 15, 1.5, 0), order=('red', 'green', 'blue')):
		""" Sequentially stacks blocks
		:params dict blocks: dictionary of blocks with keys as color and items as poses (x_c, y_c, rotation_angle)
		:params
		"""
		if not self.is_moving and not self.executing:
			try:
				pose = blocks[order[self.current_block]]  # check if block is in dict and retrieve its pose
				if self._destination_reached(pose, stack_pose):
					self.current_block += 1
				else:
					if self.stack_height > 0:
						stack_pose[2] = stack_pose[2] + (self.current_block * 1.5)  # add height of blocks to z position
					self.pick_and_place(pose, stack_pose)  # Perform pick and place operation
			except KeyError:
				self.current_block += 1  # If block is not present move to next block in stacking order

	# def sort(self, blocks, order=('red','green','blue')):

	def pick_and_place(self, pose, new_pose, raise_height=5):
		""" Picks up a block and places it somewhere
		:params tuple pose: (x_center, y_center, rotation_angle) for block
		:params tuple new_pose: (x_new, y_new, z_new, rotation_angle) for block
		"""
		# Start execution of a sequence of actions
		self.executing = True

		# Lower arm
		self.move_arm(pose[0], pose[1] - 2, 5, -90, -90, 0)

		# Open and rotate gripper
		self.open_gripper()
		self.rotate_gripper(getAngle(pose[0], pose[1], pose[2]))

		# Move into grabbing position
		self.move_arm(pose[0], pose[1], 1.5, -90, -90, 0)

		# Close gripper
		self.close_gripper()

		# Lift block
		self.move_arm(pose[0], pose[1], raise_height, -90, -90, 0)

		# Move block to (x, y, z)
		self.move_arm(new_pose[0], new_pose[1], new_pose[2], -90, -90, 0)

		# Rotate gripper and release
		self.rotate_gripper(getAngle(new_pose[0], new_pose[1], new_pose[3]))
		self.open_gripper()

		# Move arm back to home for better camera visibility
		self.move_arm(0, 10, 10, -30, -30, -90)

		# No longer executing sequence of actions
		self.executing = False

	def move_arm(self, x, y, z, a0, a1, a2):
		self.arm.setPitchRangeMoving((x, y, z), a0, a1, a2)
		self.moving = True
		time.sleep(0.2)
		self.moving = False

	def open_gripper(self):
		Board.setBusServoPulse(1, self.servo1 - 280, 500)
		self.grasping = False  # Always true
		self.moving = True
		time.sleep(2)
		self.moving = False

	def close_gripper(self):
		Board.setBusServoPulse(1, self.servo1 - 50, 500)
		self.grasping = True  # Sometimes true
		self.moving = True
		time.sleep(2)
		self.moving = False

	def rotate_gripper(self, angle):
		Board.setBusServoPulse(2, angle, 500)
		self.moving = True
		time.sleep(2)
		self.moving = False

	def reset(self):
		self.close_gripper()
		self.rotate_gripper(500)
		self.move_arm(0, 10, 10, -30, -30, -90)

	@staticmethod
	def _destination_reached(pose, desired_pose):
		dist = sqrt((pose[0] - desired_pose[0]) ** 2 + (pose[1] - desired_pose[1]) ** 2)
		if dist > 5:
			return False
		return True


if __name__ == "__main__":
	mp = Motion()

	# mp.move_arm(1, 20, 15, 0, -90, 0)
	# mp.reset()
	# mp.move_arm(-10, 25, 2, 0, 0, -90)
	# time.sleep(1)
	# mp.move_arm(10, 10, 5, 0, 0, 0)
	# time.sleep(1)
	# mp.move_arm(-10, 10, 10, 0, 0, 0)

	# mp.open_gripper()
	# mp.close_gripper()
	# mp.rotate_gripper(90)
	# mp.pick_and_place((-15 + 0.5, 12 - 0.5, -90), (-1.66, 15, 1.5, -62.5)
	# mp.pick_and_place((-1.66, 15, -62.5), (-15 + 0.5, 12 - 0.5, 1.5, -90))

	mp.move_arm(sys.argv[1:])
	mp.reset()