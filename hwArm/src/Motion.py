#!/usr/bin/python3
import sys
import cv2
import time

# from LABConfig import *
from armpi_fpv_kinematics.kinematics import ik_transform

class Motion:
	def __init__(self) -> None:
		# servo position val
		self.servo1 = 500

		# IK solver and motion planner/exector
		self.arm = ik_transform.ArmIK()

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

	def move_arm(self, x, y, z, a0, a1, a2):
		self.arm.setPitchRanges((x, y, z), a0, a1, a2)
		self.moving = True
		time.sleep(0.2)
		self.moving = False

	# def open_gripper(self):
	# 	Board.setBusServoPulse(1, self.servo1 - 280, 500)
	# 	self.grasping = False  # Always true
	# 	self.moving = True
	# 	time.sleep(2)
	# 	self.moving = False
	#
	# def close_gripper(self):
	# 	Board.setBusServoPulse(1, self.servo1 - 50, 500)
	# 	self.grasping = True  # Sometimes true
	# 	self.moving = True
	# 	time.sleep(2)
	# 	self.moving = False
	#
	# def rotate_gripper(self, angle):
	# 	Board.setBusServoPulse(2, angle, 500)
	# 	self.moving = True
	# 	time.sleep(2)
	# 	self.moving = False

	def reset(self):
		# self.close_gripper()
		# self.rotate_gripper(500)
		self.move_arm(0, 10, 10, -30, -30, -90)


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