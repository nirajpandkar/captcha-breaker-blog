import imutils
import cv2

def preprocess(image, width, height):
	(h, w) = image.shape[:2]

	# resize the dimension which is greater of the two (height/width)
	if w > h:
		image = imutils.resize(image, width=width)

	else:
		image = imutils.resize(image, height=height)

	# determine the padding values for the width and height to
	# obtain the target dimensions
	padW = int((width - image.shape[1]) / 2.0)
	padH = int((height - image.shape[0]) / 2.0)

	# pad the image then apply one more resizing to handle any
	# rounding issues
	image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
	cv2.BORDER_REPLICATE)
	image = cv2.resize(image, (width, height))

	# return the pre-processed image
	return image




# If you want to see the difference between the resizing functionality provided by imutils vs cv2
# if __name__ == '__main__':
# 	img = cv2.imread("dataset/1/0001.png")
# 	img_pre = preprocess(img, 28, 28)
# 	img_cv2resize = cv2.resize(img, (28, 28))
# 	img_arresize = imutils.resize(img, height=28)
# 	print(img_pre.shape)
# 	cv2.imshow("Original", img)
# 	cv2.imshow("Preprocessed", img_pre)
# 	cv2.imshow("CV2 Resize", img_cv2resize)
# 	cv2.imshow("AR Resize", img_arresize)


# 	cv2.waitKey(0)