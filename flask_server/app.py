import io
import flask
import base64
import tf_wrapper as tfw
import datetime
import os
from PIL import Image

app = flask.Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/hello", methods=["GET", "POST"])
def hello_world():
    resp = "Hello<br>Time: " + str(datetime.datetime.now()) + "<br>Process ID: " + str(os.getpid())
    return resp


@app.route("/predict", methods=["POST", "GET"])
def predict():
    message = ""
    if flask.request.method == "POST":
        message = "no files attached"
        if flask.request.files.get("image"):
            # read the image in PIL format
            image_bytes = flask.request.files["image"].read()
            byte_stream = io.BytesIO(image_bytes)
            pil_image = Image.open(byte_stream)
            message = "method file upload"
        elif flask.request.form and flask.request.form['image_b64']:
            b64_image = flask.request.form['image_b64']
            decoded_image = base64.b64decode(b64_image)
            byte_stream = io.BytesIO(decoded_image)
            pil_image = Image.open(byte_stream)
            message = "method file b64 encoding"
        elif flask.request.data != None:
            pil_image = Image.open(flask.request.data)
            message = "image in data"


    # resp = tfw.predict(pil_image, "faster_rcnn_inception_resnet_v2_atrous_oid")
    return flask.render_template("index.html", message=message, title="CZ POC")


if __name__ == "__main__":
    print("Starting server")
    app.run(debug=True)
