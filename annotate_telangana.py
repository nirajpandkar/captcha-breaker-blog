import cv2 
import imutils
import numpy as np
import argparse
import os

from clean_image import clean_image_telangana
import traceback

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
help="path to input directory of images")
ap.add_argument("-a", "--annot", required=True,
help="path to output directory of annotations")
args = vars(ap.parse_args())

def annotate_digit(x, y, w, h, parts, final_output, counts):
	"""
	Shows an image of a digit, waits for input key and saves the image in the appropriate digit folder.

	Arguments:

	x, y, w, h = x, y coordinates and width and height obtained from cv2.boudingRect() function.
	parts = the number of parts a particular contour is to be divided into.
	final_output = a cv2 image which has been processed properly for ROI generation
	counts = dictionary to store/retrieve number of images annotated per digit 
	"""
	part = int(w/parts)

	cv2.imshow("final", final_output)
	for i in range(parts):

		# Isolating the region of interest - the digit
		roi = final_output[y:y + h, x + part*i:x + part*(i+1)]

		# Creatinga a black border around the image to avoid the image sticking to the borders 
		# (to give the digit some breathing space)
		roi = cv2.copyMakeBorder(roi, 5, 5, 5, 5, cv2.BORDER_CONSTANT, 0)

		# After isolating, remove small unnecessary blobs, dots. 
		# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
		# roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)

		# Show image for annotation and wait for input key
		cv2.imshow("ROI", roi)
		key = cv2.waitKey(0)
		
		# If the image is garbage, skip it with back tick
		if key == ord("`"):
			continue

		# Obtain the input key and write that image to disk under the appropriate digit folder
		key = chr(key).upper()
		print(key)
		dirPath = os.path.sep.join([args["annot"], key])
		if not os.path.exists(dirPath):
			os.makedirs(dirPath)
		count = counts.get(key, 1)
		p = os.path.sep.join([dirPath, "{}.png".format(str(count).zfill(4))])
		cv2.imwrite(p, roi)

		counts[key] = count + 1

images_path_list = os.listdir(args["input"])
counts = {}
# images_path_list = ['1190.png']
for j, image in enumerate(images_path_list):

	print("[INFO] processing image {}/{}".format(j + 1, len(images_path_list)))
	print(image)

	try:
		img = cv2.imread("{}/".format(args["input"]) + image)

		final_output = clean_image_telangana(img)
		cv2.imshow("cleaned image", final_output)
		cv2.waitKey(0)
		cnts = cv2.findContours(final_output.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[1]
		predictions = {}

		# set height and width of a digit and number of digits
		w_digit = 10
		h_digit = 12
		n_digits = 6

		# Iterate through the contours
		for c in cnts:
			(x, y, w, h) = cv2.boundingRect(c)
			#print(x,y,w,h)
			# If the contour height is less than the normal digit height, treat as an unnecessary blob and skip
			if(h < h_digit):
				dropped_x = x
				continue
			
			# Initialize
			parts=1

			# Depending on the width of the contour, decide on the number of parts for it to be divided into. 
			if(w > (w_digit*6)- 5):
				parts = 6
			elif(w > (w_digit*5)-5 and w < (w_digit*6)- 5):
				parts = 5
			elif(w > (w_digit*4)-5 and w < (w_digit*5) - 5):
				parts = 4
			elif(w > (w_digit*3)-5 and w <  + (w_digit*4)- 5):
				parts = 3
			elif(w > (w_digit*2)-5 and w <  + (w_digit*3)- 5):
				parts = 2
			else:
				parts = 1

			annotate_digit(x, y, w, h, parts, final_output, counts)
	except KeyboardInterrupt:
		print("[INFO] manually leaving script")
		break

	# an unknown error has occurred for this particular image
	except:
		print("[INFO] skipping image...")
		print(traceback.format_exc())