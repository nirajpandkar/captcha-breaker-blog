import cv2 
import imutils
import numpy as np
import argparse
import os
from preprocess_image import preprocess
from keras.models import load_model
from clean_image import clean_image_telangana
import tensorflow as tf
import glob
import traceback
import pytesseract

global model

# Used for Telangana
model_patna = load_model("patna_baseline.h5")

# this is key : save the graph after loading the model
global graph
graph = tf.get_default_graph()


def prepare_image_telangana(x, y, w, h, parts, final_output, predictions):
	"""
	Updates "predictions" dictionary with digit prediction corresponding to the appropriate "x" value.

	Arguments:
	x, y, w, h = x, y coordinates and width and height obtained from cv2.boudingRect() function.
	parts = the number of parts a particular contour is to be divided into.
	final_output = a cv2 image which has been processed properly for ROI generation
	predictions = A dictionary with x coordinates as keys and the digit prediction at the corresponding 
				  x coordinate as value 
	"""
	 
	part = int(w/parts)
	for i in range(parts):

		# Isolating the region of interest - the digit
		# Also, y shouldn't go beyond image (negative y)
		roi = final_output[y:y + h, x + part*i:x + part*(i+1)]

		# Creatinga a black border around the image to avoid the image sticking to the borders 
		# (to give the digit some breathing space)
		roi = cv2.copyMakeBorder(roi, 5, 5, 5, 5, cv2.BORDER_CONSTANT, 0)
		# cv2.imshow("ROI", roi)
		# cv2.waitKey(0)
		# After isolating, remove small unnecessary blobs, dots. 
		# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
		# roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)

		# Preprocess the image to a 28x28 dimension and add the digit prediction to a dictionary with x values
		# as keys. This inherently sorts the predicted digits in the right order. 
		image = preprocess(roi, 28, 28)/255.0
		with graph.as_default():
			predictions[x + part * i] = np.argmax(model_patna.predict(image.reshape(1,28,28,1)))

def predict_captcha_telangana(img):
	"""
	Returns the captcha string. 

	Arguments:

	A cv2 image object. 
	"""
	final_output = clean_image_telangana(img)
	
	cnts = cv2.findContours(final_output.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[1]
	predictions = {}

	# set height and width of a digit and number of digits
	w_digit = 10
	h_digit = 12
	n_digits = 6

	# Iterate through the contours
	#print("Number of contours: ", len(cnts))
	for c in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		#print(x,y,w,h)
		# If the contour height is less than the normal digit height, treat as an unnecessary blob and skip
		if((h < h_digit) or (h > h_digit + 2)):
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
		prepare_image_telangana(x, y, w, h, parts, final_output, predictions)
	
	keys = predictions.keys()

	# If there are less keys than the number of digits required, assume that one of the digit's contours 
	# has been divided into multiple contours and set that digit as 5 (Decided on 5 because that was the digit
	# which caused the most trouble in finding contours and which was mostly predicted wrong)

	captcha = "".join(str(predictions[key]) for key in sorted(keys))
	return captcha

if __name__ == '__main__':

	images_path_list = glob.glob("CaptchaImages/*")
	print(images_path_list)
	# images_path_list = ['PatnaCaptchaScreenShots/942.png']
	for j, image in enumerate(images_path_list):
		print(image)
		img = cv2.imread(image)
		cv2.imshow("Original Image", img)
		predicted_captcha = predict_captcha_telangana(img)
		print("Captcha: {}".format(predicted_captcha))

		key = cv2.waitKey(0)

		# If the image is garbage, skip it with back tick
		if key == ord("`"):
			continue

		if key == ord("/"):
			exit()

		# Obtain the input key and write that image to disk under the appropriate digit folder
		key = chr(key).upper()
		print(key)
		dirPath = os.path.sep.join(["CorrectIncorrect", key])
		if not os.path.exists(dirPath):
			os.makedirs(dirPath)
		p = os.path.sep.join([dirPath, "{}.png".format(str(predicted_captcha))])
		cv2.imwrite(p, img)