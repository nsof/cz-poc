import io
import flask
import base64
import datetime
import os
import json
from PIL import Image
import werkzeug.utils
import tf_wrapper as tfw

app = flask.Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/hello", methods=["GET", "POST"])
def hello_world():
    resp = "Hello<br>Time: " + str(datetime.datetime.now()) + "<br>Process ID: " + str(os.getpid())
    return resp

@app.route("/analyze", methods=["GET"])
def analyze():
    return flask.render_template("analyze.html", title="CZ POC")

# REST API
@app.route("/predict", methods=["POST"])
def predict():
    if flask.request.files.get("image"):
        image_bytes = flask.request.files["image"].read()
        byte_stream = io.BytesIO(image_bytes)
    elif flask.request.form and flask.request.form['image_b64']:
        b64_image = flask.request.form['image_b64']
        decoded_image = base64.b64decode(b64_image)
        byte_stream = io.BytesIO(decoded_image)

    if byte_stream != None:
        original_image = Image.open(byte_stream)
        original_image.filename = werkzeug.utils.secure_filename(flask.request.form["imagename"])

        # ROOT_FOLDER = "flask_server/"
        # DATA_FOLDER = "data/"
        # local_image_filename_prefix = datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S.%f.")
        # image_name = local_image_filename_prefix + pil_image.filename
        # local_image_filepath = os.path.join(ROOT_FOLDER+DATA_FOLDER, image_name)
        # pil_image.save(local_image_filepath)
        analyzed_image, predictions = tfw.predict(original_image, "faster_rcnn_inception_resnet_v2_atrous_oid")
        if analyzed_image == None or predictions == None:
            jsonResponse = { "error": True }
        else:
            # analyzed_image, predictions = original_image.copy(), [{"score": 0.9, "class":"bunny" },{"score": 0.8, "class":"unicorn" }]

            # analyzed_image_name = local_image_filename_prefix + "analyzed." + pil_image.filename
            # analyzed_image_filepath = os.path.join(ROOT_FOLDER+DATA_FOLDER, analyzed_image_name)
            # pil_image.save(analyzed_image_filepath)
            # analyzed_image_url = DATA_FOLDER + analyzed_image_name

            bytesstream = io.BytesIO()
            # original_image.save(bytesstream, format="JPEG")
            # original_image_b64string = (base64.b64encode(bytesstream.getvalue())).decode("utf-8")
            # bytesstream.truncate(0)
            # bytesstream.seek(0)
            analyzed_image.save(bytesstream, format="JPEG")
            analyzed_image_b64string = (base64.b64encode(bytesstream.getvalue())).decode("utf-8")

            jsonResponse = {
                "error": False,
                "predictions": predictions,
                # "original_image": original_image_b64string,
                "analyzed_image": analyzed_image_b64string
            }
    else:
        jsonResponse = { "error": True }

    return json.dumps(jsonResponse)


if __name__ == "__main__":
    print("Starting server")
    app.run(debug=True)
