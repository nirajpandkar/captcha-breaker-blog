import cv2
import requests
import os
import time
from tqdm import tqdm
import traceback

def call_endpoint(image_path):
	# os.system("wget -U \"Opera 11.0\" http://elegalix.allahabadhighcourt.in/elegalix/Code.jpg -O test.jpg")
	image_path = "SupremeCourtCaptchaScreenShots/" + image_path
	image = open(image_path, 'rb').read()
	start = time.time()
	r = requests.post("http://localhost:4545/supremecourt", files={"image":image}).json()
	print(r)
	end = time.time()
	return end-start
	# print(r["predicted_captcha"])

if __name__ == '__main__':
	image_list = os.listdir("./SupremeCourtCaptchaScreenShots")
	times = list()
	try:
		for image in tqdm(image_list):
			time_taken = call_endpoint(image)
			times.append(time_taken)
			print("File {} done in {}".format(image, time_taken))
			break
		print("Total time: ", sum(times))
	except Exception as e:
		print("[EXCEPTION]: ", e)
		print(traceback.format_exc())