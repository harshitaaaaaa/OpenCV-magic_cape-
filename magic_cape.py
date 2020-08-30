#import libraries

import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

time.sleep(2)

background = 0

#Capturing the background
for i in range(30):

	ret, background = cap.read()

	#flip the image

	#background = np.flip(background, axis=1)

while(cap.isOpened()):

	ret, img = cap.read()

	if not ret:
		break

	# img = np.flip(ig, axis=1)

# Converting from BGR to HSV
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)	#HSB

	lower_red = np.array([0, 120, 70])
	upper_red = np.array([10, 255, 255])
	mask1 = cv2.inRange(hsv, lower_red, upper_red)	#separating the clock part

	lower_red = np.array([0, 120, 70])
	upper_red = np.array([10, 255, 255])
	mask2 = cv2.inRange(hsv, lower_red, upper_red)

	mask1 = mask1 + mask2 

	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 2)	# Noise removal
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iterations = 1)

	mask2 = cv2.bitwise_not(mask1)

	res1 = cv2.bitwise_and(background, background, mask = mask1)	#used for segmentation of the color
	res2 = cv2.bitwise_and(img, img, mask=mask2)	# Used to substitute the cloak part
	final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

	cv2.imshow('Eureka !!', final_output)
	k = cv2.waitKey(0)
	if k == 27:
		break

	cap.release()
	cv2.destroyAllWindows()
