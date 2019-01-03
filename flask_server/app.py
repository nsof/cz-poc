import io
import flask
import base64
import tf_wrapper as tfw
from PIL import Image

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    return '\nHello, World!\n\n'


@app.route("/predict", methods=["POST"])
def predict():
    if flask.request.files.get("image"):
        # read the image in PIL format
        image_bytes = flask.request.files["image"].read()
        byte_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(byte_stream)

    #     results, image_out = detector.detect_in_image(image)
    elif flask.request.form['image_b64']:
        b64_image = flask.request.form['image_b64']
        decoded_image = base64.b64decode(b64_image)
        byte_stream = io.BytesIO(decoded_image)
        pil_image = Image.open(byte_stream)
    else:
        print ("no files attached")
        return "no files attached"

    tfw.predict(pil_image, "faster_rcnn_inception_resnet_v2_atrous_oid")
    return "done predicting"


if __name__ == "__main__":
    print(("Starting server from the cli"))
    app.run(debug=True)
