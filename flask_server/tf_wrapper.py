import argparse
import json
import sys
import requests
import numpy as np

def predict(pil_image, model_name):
    # pil_image.thumbnail((299, 299))
    np_array_image = np.array(pil_image) / 255.0
    array_image = np_array_image.tolist()
    if model_name == "inception_resnet_v2":
        payload = {
            "instances": [{'input_image': array_image}]
        }
    else:
        payload = {
            "instances": [{'inputs': array_image}]
        }

    # sending post request to TensorFlow Serving server
    url = f"http://localhost:8501/v1/models/{model_name}:predict"
    print (f"sending to: {url}")
    r = requests.post(url, json=payload, timeout=None)
    if r.status_code != 200:
        print ("error making request")
    else:
        pred = json.loads(r.content.decode('utf-8'))
    print (r.text)


if __name__ == "__main__":
    # Argument parser for giving input image_path from command line
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False, help="path of the image", default=r"C:\dev\tf\tf\data\posing.jpg")
    ap.add_argument("-m", "--model", required=False, help="model name", default="faster_rcnn_inception_resnet_v2_atrous_oid")
    args = vars(ap.parse_args())
    image_path = args['image']
    model_name = args['model']
    predict(image_path, model_name)
