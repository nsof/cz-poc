import time
import argparse
import json
import sys
import requests
import numpy as np
from image_utils import ImageUtils

config = None

_relevant_classifications = [
    b'Backpack',
    b'Belt',
    b'Boot',
    b'Brassiere',
    b'Briefcase',
    b'Clothing',
    b'Coat',
    b'Cowboy hat',
    b'Crown',
    b'Dress',
    b'Earrings',
    b'Fashion accessory',
    b'Fedora',
    b'Footwear',
    b'Glasses',
    b'Glove',
    b'Goggles',
    b'Handbag',
    b'Hat',
    b'Helmet',
    b'High heels',
    b'Human hair',
    b'Jacket',
    b'Jeans',
    b'Lifejacket',
    b'Luggage and bags',
    b'Miniskirt',
    b'Necklace',
    b'Roller skates',
    b'Sandal',
    b'Scarf',
    b'Shirt',
    b'Shorts',
    b'Skirt',
    b'Sock',
    b'Sombrero',
    b'Sports equipment',
    b'Sports uniform',
    b'Suit',
    b'Suitcase',
    b'Sun hat',
    b'Sunglasses',
    b'Swim cap',
    b'Swimwear',
    b'Tiara',
    b'Tie',
    b'Trousers',
    b'Umbrella',
    b'Watch'
]


def _convert_to_array(results):
    classes = results["detection_class_entities"]
    scores = results["detection_scores"]
    boxes = results["detection_boxes"]
    arr = [{"class": classes[i], "score": scores[i], "box": boxes[i]} for i in range(len(boxes))]
    return arr


def _filter_results(results, n, min_score, classes_to_keep):
    filtered_results = []
    for i in range(min(len(results), n)):
        result = results[i]
        if result["score"] < min_score:
            continue
        if classes_to_keep and result["class"] not in classes_to_keep:
            continue
        filtered_results.append(result)

    return filtered_results

def get_url(host_name="localhost", model_name="faster_rcnn_inception_resnet_v2_atrous_oid"):
    
    url = f"http://{host_name}:8501/v1/models/{model_name}:predict"
    return url

def predict_inception_resnet_v2(pil_image, filter=True):
    pil_image.thumbnail((299, 299))
    np_array_image = np.array(pil_image)
    np_array_image = np_array_image / 255.0
    array_image = np_array_image.tolist()

    payload = {
        "instances": [{'input_image': array_image}]
    }
    
    url = get_url(config["HOST"], "inception_resnet_v2")
    print(f"sending to: {url}")

    r = requests.post(url, json=payload, timeout=None)

    if r.status_code != 200:
        print(f"error making request.\n {r.text}")
        sys.stdout.flush()
        image_with_boxes = None
        results = None
    else:
        results = r.content.decode('utf-8')
        print(f"Results: {results}")
        image_with_boxes = pil_image

    return image_with_boxes, results

def predict_faster_rcnn_inception_resnet_v2_atrous_oid(pil_image, model_name, filter=True):
    prepared_image = ImageUtils.prepare_image(pil_image, 320, 240)
    np_array_image = np.array(prepared_image)
    array_image = np_array_image.tolist()

    payload = {
        "instances": [{'inputs': array_image}]
    }

    url = get_url(config["HOST"], "faster_rcnn_inception_resnet_v2_atrous_oid")
    print(f"sending to: {url}")

    r = requests.post(url, json=payload, timeout=None)

    if r.status_code != 200:
        print(f"error making request.\n {r.text}")
        sys.stdout.flush()
        image_with_boxes = None
        results = None
    else:
        results = r.content.decode('utf-8')
        print("Found %d objects." % len(results["detection_scores"]))
        print("Inference took %.2f seconds." % (time.clock()-start_time))
        sys.stdout.flush()
        results = _convert_to_array(results)
        if filter:
            results = _filter_results(results, 50, 0.1, _relevant_classifications)
        else:
            results = _filter_results(results, 100, 0.1, None)

        image_with_boxes_array = ImageUtils.draw_boxes(pil_image, results)
        image_with_boxes = Image.fromarray(image_out)

    return image_with_boxes, results

def predict(pil_image, model_name, filter=True):
    start_time = time.clock()
    print("Starting inference")
    sys.stdout.flush()
    if model_name == "inception_resnet_v2":
        predictor = predict_inception_resnet_v2
    else:
        predictor = predict_faster_rcnn_inception_resnet_v2_atrous_oid

    image_with_boxes, results = predictor(pil_image, filter)

    return image_with_boxes, results


def load_config(env):
    with open(r"flask_server\config.json", "r") as f:
        all_envs_config = json.load(f)
        global config
        if env in all_envs_config:
            config = all_envs_config[env]
        else:
            config = all_envs_config["DEFAULT"]
    
load_config("")


if __name__ == "__main__":
    from PIL import Image
    # Argument parser for giving input image_path from command line
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False, help="path of the image", default=r"C:\dev\tf\tf\data\posing.jpg")
    ap.add_argument("-m", "--model", required=False, help="model name", default="faster_rcnn_inception_resnet_v2_atrous_oid")
    args = vars(ap.parse_args())
    image_path = args['image']
    model_name = args['model']
    # model_name = "inception_resnet_v2"

    image = Image.open(image_path)
    

    predict(image, model_name)

