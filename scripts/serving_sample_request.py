import argparse
import json
import sys

import numpy as np
import requests
# from keras.applications import inception_v3
from keras.preprocessing import image

def predict(host_name, image_path, model_name):
    # Preprocessing our input image
    img = image.img_to_array(image.load_img(image_path, target_size=(224, 224))) / 255.
    # this line is added because of a bug in tf_serving(1.10.0-dev)

    if model_name == "inception_resnet_v2":
        img = img.astype('float16')
        payload = {
            "instances": [{'input_image': img.tolist()}],
        }
    else:
        img = img.astype('uint8')
        payload = {
            "instances": [{'inputs': img.tolist()}]
        }

    # sending post request to TensorFlow Serving server
    url = f"http://{host_name}:8501/v1/models/{model_name}:predict"
    print (f"sending to: {url}")
    r = requests.post(url, json=payload, timeout=None)
    if r.status_code != 200:
        print ("error making request")
        print (r.text)
    else:
        print (r.text)
        pred = json.loads(r.content.decode('utf-8'))
        # Decoding the response
        # decode_predictions(preds, top=5) by default gives top 5 results
        # You can pass "top=10" to get top 10 predicitons
        # print(json.dumps(inception_v3.decode_predictions(np.array(pred['predictions']), top=25)[0]))


if __name__ == "__main__":
    # Argument parser for giving input image_path from command line
    ap = argparse.ArgumentParser()
    ap.add_argument("-H", "--Host", required=False, help="host name", default="localhost")
    ap.add_argument("-i", "--image", required=False, help="path of the image", default=r"C:\dev\tf\tf\data\posing.jpg")
    ap.add_argument("-m", "--model", required=False, help="model name", default="faster_rcnn_inception_resnet_v2_atrous_oid")
    args = vars(ap.parse_args())
    image_path = args['image']
    model_name = args['model']
    host_name = args['Host']
    predict(host_name, image_path, model_name)
