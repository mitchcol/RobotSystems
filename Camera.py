import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import logging
import math

# NOTE: All of this code was copied from the link provided in the lab manual. I refactored the variable names and
# packed the code into a class

class Camera():
	# constructor
	def __init__(self, resolution=(640, 480), framerate=24):
		self._camera = PiCamera()
		self._camera.resolution = resolution
		self._camera.framerate = framerate

		self._rawCapture = PiRGBArray(self._camera, size=self._camera.resolution)

	# getters/setters
	@property
	def camera(self):
		return self._camera

	@property
	def rawCapture(self):
		return self._rawCapture

	# member methods
	def getBlueMask(self, frame):
		# setting the lower and upper blue color bounds
		lowerBlue = np.array([60, 40, 40])
		upperBlue = np.array([150, 255, 255])

		# converting frame to hvs
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		return cv2.inRange(hsv, lowerBlue, upperBlue)

	def detectEdges(self, frame):
		# filter for blue lane lines
		mask = self.getBlueMask(frame)

		# detect edges
		edges = cv2.Canny(mask, 200, 400)

		return edges

	def filterROI(self, edges):
		height, width = edges.shape
		mask = np.zeros_like(edges)

		# only focus bottom half of the screen
		polygon = np.array([[
			(0, height * 1 / 2),
			(width, height * 1 / 2),
			(width, height),
			(0, height),
		]], np.int32)

		cv2.fillPoly(mask, polygon, 255)
		croppedEdges = cv2.bitwise_and(edges, mask)
		return croppedEdges

	def detectLineSegments(self, croppedEdges):
		# tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
		rho = 1  # distance precision in pixel, i.e. 1 pixel
		angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
		minThreshold = 10  # minimal of votes
		lineSegments = cv2.HoughLinesP(croppedEdges, rho, angle, minThreshold,
										np.array([]), minLineLength=8, maxLineGap=4)

		return lineSegments

	def avgSlopeIntercept(self, frame, lineSegments):
		"""
		This function combines line segments into one or two lane lines
		If all line slopes are < 0: then we only have detected left lane
		If all line slopes are > 0: then we only have detected right lane
		"""
		laneLines = []
		if lineSegments is None:
			logging.info('No line_segment segments detected')
			return laneLines

		height, width, _ = frame.shape
		left_fit = []
		right_fit = []

		boundary = 1 / 3
		leftRegionBoundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
		rightRegionBoundary = width * boundary  # right lane line segment should be on left 2/3 of the screen

		for lineSegment in lineSegments:
			for x1, y1, x2, y2 in lineSegment:
				if x1 == x2:
					logging.info('skipping vertical line segment (slope=inf): %s' % lineSegment)
					continue
				fit = np.polyfit((x1, x2), (y1, y2), 1)
				slope = fit[0]
				intercept = fit[1]
				if slope < 0:
					if x1 < leftRegionBoundary and x2 < leftRegionBoundary:
						left_fit.append((slope, intercept))
				else:
					if x1 > rightRegionBoundary and x2 > rightRegionBoundary:
						right_fit.append((slope, intercept))

		leftFitAvg= np.average(left_fit, axis=0)
		if len(left_fit) > 0:
			laneLines.append(self.makePoints(frame, leftFitAvg))

		rightFitAvg = np.average(right_fit, axis=0)
		if len(right_fit) > 0:
			laneLines.append(self.makePoints(frame, rightFitAvg))

		logging.debug('lane lines: %s' % laneLines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]

		return laneLines

	def makePoints(self, frame, line):
		height, width, _ = frame.shape
		slope, intercept = line
		y1 = height  # bottom of the frame
		y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

		# bound the coordinates within the frame
		x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
		x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
		return [[x1, y1, x2, y2]]

	def detectLane(self, frame):
		edges = self.detectEdges(frame)
		croppedEdges = self.filterROI(edges)
		lineSegments = self.detectLineSegments(croppedEdges)
		laneLines = self.avgSlopeIntercept(frame, lineSegments)

		return laneLines

	def getSteeringAngle(self, frame, laneLines):
		height, width, _ = frame.shape

		if len(laneLines) == 2:
			_, _, leftX2, _ = laneLines[0][0]
			_, _, rightX2, _ = laneLines[1][0]
			mid = int(width / 2)
			xOffset = (leftX2 + rightX2) / 2 - mid
			yOffset = int(height / 2)
		elif len(laneLines) == 1:
			x1, _, x2, _ = laneLines[0][0]
			xOffset = x2 - x1
			yOffset = int(height / 2)
		else:
			xOffset = 0
			yOffset = 1

		midRadianAngle = math.atan(xOffset / yOffset)  # angle (in radian) to center vertical line
		midDegAngle = int(midRadianAngle * 180.0 / math.pi)  # angle (in degrees) to center vertical line
		steeringAngle = midDegAngle + 90  # this is the steering angle needed by picar front wheel

		# normalizing the steering angle that is calculated to +- 30 degrees
		

		return steeringAngle

	def displayLaneLines(self, frame, lines, lineColor=(0, 255, 0), lineWidth=2):
		lineImage = np.zeros_like(frame)

		if lines is not None:
			for line in lines:
				for x1, y1, x2, y2 in line:
					cv2.line(lineImage, (x1, y1), (x2, y2), lineColor, lineWidth)

		lineImage = cv2.addWeighted(frame, 0.8, lineImage, 1, 1)
		return lineImage

	def displayHeadingLine(self, frame, steeringAngle, lineColor=(0, 0, 255), lineWidth=5):
		headingImage = np.zeros_like(frame)
		height, width, _ = frame.shape

		# figure out the heading line from steering angle
		# heading line (x1,y1) is always center bottom of the screen
		# (x2, y2) requires a bit of trigonometry

		# Note: the steering angle of:
		# 0-89 degree: turn left
		# 90 degree: going straight
		# 91-180 degree: turn right
		steering_angle_radian = steeringAngle / 180.0 * math.pi
		x1 = int(width / 2)
		y1 = height
		x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
		y2 = int(height / 2)

		cv2.line(headingImage, (x1, y1), (x2, y2), lineColor, lineWidth)
		headingImage = cv2.addWeighted(frame, 0.8, headingImage, 1, 1)

		return headingImage
