import cv2
import numpy as np
from imutils import paths
from itertools import islice

def localize(img):
	"""
	Localize text in a black and white image
	"""
	# # Crop the image to eliminate border
	# h, w, c = img.shape

	# start_x = int(0.12*w)
	# start_y = int(0.15*h)

	# img = img[start_y: h - start_y, start_x: w - start_x]

	# #make image gray 
	# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	# #Blur
	# blur = cv2.GaussianBlur(gray,(5,5),0)

	# sobel = cv2.Sobel(blur, -1, 1, 0)
	# cv2.imshow("Sobel", sobel)

	# #Thresholding
	# thresh = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU)[1]
	# cv2.imshow("Thresh", thresh) 

	
	thresh = clean_image_patna(img)
	cv2.imshow("Original", thresh)
	height, width = thresh.shape
	
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16,4))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) 

	cnts = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]

	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)
		cv2.rectangle(thresh,(x,y),(x+w,y+h),(255,255,255),1)
		cv2.line(thresh, (x + (w/3), y), (x + (w/3), y+h), (255,255,255), 1)
		cv2.line(thresh, (x+(2*w/3), y), (x+(2*w/3), y+h), (255,255,255), 1)
	return closed, thresh

def clean_image_telangana(img):
	#make image gray 
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#cv2.imshow("Gray", gray)
	#Thresholding
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
	#cv2.imshow("Thresholding", thresh)

	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,2))
	erode = cv2.erode(thresh, kernel, iterations = 1)
	#cv2.imshow("Erode", erode)

	return erode

def view(image):
	img = cv2.imread(image)
	cv2.imshow("Original", np.hstack([img]))
	img_s = clean_image_telangana(img)
	cv2.imshow("Final Output", np.hstack([img_s]))
	# cv2.imshow("Bounding Box", rect)

	cv2.waitKey(0)

if __name__ == '__main__':
	# list_images = paths.list_images("../PatnaCaptcha/PatnaCaptchaScreenShots")
	# for image in list_images:
	# 	img = cv2.imread(image)
	# 	img_s = localize(img)
	# 	img_o = clean_image_original(img)
	# 	cv2.imshow("Final Output", np.hstack([img_s]))
	# 	cv2.waitKey(0)
	list_images = paths.list_images("SampleImages/TelanganaCaptcha")

	
	for image in list_images:
		try:
			view(image)
		except KeyboardInterrupt:
			print("manually exiting")
			break