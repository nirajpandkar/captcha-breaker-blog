from threading import Thread
import requests
import time

api_url_endpoint = "http://localhost/predict"
IMAGE_PATH = "downloaded_images/00005.jpg"

NUM_REQUESTS = 500
SLEEP_COUNT = 0.05

def call_predict_endpoint(n):
	image = open(IMAGE_PATH, 'rb').read()
	# start = time.time()
	r = requests.post("http://13.233.32.176/app/predict", files={"image":image}).json()
 
	# ensure the request was sucessful
	if r["success"]:
		print("[INFO] thread {} OK".format(n))
 
	# otherwise, the request failed
	else:
		print("[INFO] thread {} FAILED".format(n))
 
# loop over the number of threads
for i in range(0, NUM_REQUESTS):
	# start a new thread to call the API
	t = Thread(target=call_predict_endpoint, args=(i,))
	t.daemon = True
	t.start()
	time.sleep(SLEEP_COUNT)
 
# insert a long sleep so we can wait until the server is finished
# processing the images
time.sleep(100)