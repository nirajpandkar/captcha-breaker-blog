import flask
from predict import predict_captcha_patna, predict_captcha_allahabad, predict_captcha_lucknow, predict_captcha_sc
import numpy as np
import io
from PIL import Image
from keras import backend as K
import time
import traceback
import logging

app = flask.Flask(__name__)
LOG_FILENAME='captcha.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

@app.route("/")
def hello():
    return "Hello world"

@app.route("/allahabad", methods=["POST"])
def predict():
    predicted_captcha = ""
    data = dict()
    data["success"] = False
    try:
        if flask.request.method == "POST":
            if flask.request.files.get("image"):
                image = flask.request.files["image"].read()

                # Read the byte string from the POST request and convert to PIL image, 
                # which is further converted to an image format cv2 can work with. 
                pil_image = Image.open(io.BytesIO(image))
                open_cv_image = np.array(pil_image) 

                # Convert RGB to BGR 
                image = open_cv_image[:, :, ::-1].copy()
  
                predicted_captcha = predict_captcha_allahabad(image)
                logging.info("Allahabad Captcha: {}".format(predicted_captcha))
                if predicted_captcha:
                    data["predicted_captcha"] = predicted_captcha
                    data["success"] = True
        return flask.jsonify(data)
    except Exception as e:
        logging.error(traceback.format_exc())
        return flask.jsonify(data)

@app.route("/patna", methods=["POST"])
def predict_patna():
    predicted_captcha = ""
    data = dict()
    data["success"] = False
    try:
        if flask.request.method == "POST":
            if flask.request.files.get("image"):
                image = flask.request.files["image"].read()

                # Read the byte string from the POST request and convert to PIL image, 
                # which is further converted to an image format cv2 can work with. 
                pil_image = Image.open(io.BytesIO(image))
                open_cv_image = np.array(pil_image) 

                # Convert RGB to BGR. WHy tHe heLL? Caused a lot of problems. 
                #image = open_cv_image[:, :, ::-1].copy()

                predicted_captcha = predict_captcha_patna(open_cv_image)
                logging.info("Patna Captcha: {}".format(predicted_captcha))
                if predicted_captcha:
                    data["predicted_captcha"] = predicted_captcha
                    data["success"] = True
        return flask.jsonify(data)
    except Exception:
        logging.error(traceback.format_exc())
        return flask.jsonify(data)

@app.route("/supremecourt", methods=["POST"])
def predict_sc():
    predicted_captcha = ""
    data = dict()
    data["success"] = False
    try:
        if flask.request.method == "POST":
            if flask.request.files.get("image"):
                image = flask.request.files["image"].read()

                # Read the byte string from the POST request and convert to PIL image, 
                # which is further converted to an image format cv2 can work with. 
                pil_image = Image.open(io.BytesIO(image))
                open_cv_image = np.array(pil_image) 

                # Convert RGB to BGR. WHy tHe heLL? Caused a lot of problems. 
                #image = open_cv_image[:, :, ::-1].copy()

                predicted_captcha = predict_captcha_sc(open_cv_image)
                logging.info("SC Captcha: {}".format(predicted_captcha))
                if predicted_captcha:
                    data["predicted_captcha"] = predicted_captcha
                    data["success"] = True
        return flask.jsonify(data)
    except Exception:
        logging.error(traceback.format_exc())
        return flask.jsonify(data)

@app.route("/lucknow", methods=["POST"])
def predict_lucknow():
    predicted_captcha = ""
    data = dict()
    data["success"] = False
    try:
        if flask.request.method == "POST":
            if flask.request.files.get("image"):
                image = flask.request.files["image"].read()

                # Read the byte string from the POST request and convert to PIL image, 
                # which is further converted to an image format cv2 can work with. 
                pil_image = Image.open(io.BytesIO(image))
                open_cv_image = np.array(pil_image) 

                # Convert RGB to BGR 
                image = open_cv_image[:, :, ::-1].copy()
  
                predicted_captcha = predict_captcha_lucknow(image)
                logging.info("Lucknow Captcha: {}".format(predicted_captcha))
                if predicted_captcha:
                    data["predicted_captcha"] = predicted_captcha
                    data["success"] = True
        return flask.jsonify(data)
    except Exception:
        logging.error(traceback.format_exc())
        return flask.jsonify(data)

if __name__ == '__main__':
    print("Starting web service")
    app.run(host="0.0.0.0", port=4545, debug=True)
