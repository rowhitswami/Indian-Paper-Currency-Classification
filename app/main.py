from flask_cors import CORS
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
from keras.backend import set_session
import boto3
import io
from config import LABELS, ALLOWED_EXTENSIONS, AWS_ACCESS_KEY, AWS_SECRET_KEY
from config import BUCKET, UPLOAD_FOLDER, REGION_HOST, FLASK_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
CORS(app)

config = tf.ConfigProto(device_count = {'GPU': 0})
sess = tf.Session(config=config)
global graph
graph = tf.get_default_graph()
set_session(sess)

global model
model = load_model('app/model/model.h5')

def upload_file_to_s3(file, filename):
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        bucket = s3.Bucket(BUCKET)
        bucket.Object(UPLOAD_FOLDER+filename).put(Body=file)
        return True
    except FileNotFoundError:
        print("FileNotFoundError")
        return False

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def main():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No Image Found!', 'alert-danger')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading', 'alert-danger')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploaded = upload_file_to_s3(file, filename)
        if uploaded:
            image_url = get_image_link(filename)
            label = get_label(image_url)
            return render_template('index.html', image_url=image_url, prediction=label)
        else:
            flash("Couldn't upload your image. Please try again!", 'alert-danger')
            return redirect(request.url)
    else:
        flash('Allowed image types are -> png, jpg, jpeg', 'alert-danger')
        return redirect(request.url)

def get_label(image_url):
    global sess
    global graph
    processed_image = process_image(image_url)
    with graph.as_default():
        set_session(sess)
        classes = model.predict(processed_image)
    label_classes = zip(LABELS, classes.tolist()[0])
    max_label_class = sorted(label_classes, key = lambda t: t[1])[-1]
    label = max_label_class[0]
    return label

def process_image(image_url):
    with urllib.request.urlopen(image_url) as url:
        img = load_img(io.BytesIO(url.read()), target_size=(150, 150))
        img = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
        img = img.reshape(1,150,150,3).astype('float')
        img /= 255
        return img

def get_image_link(filename):
    return "https://indian-currency-prediction.s3.ap-south-1.amazonaws.com/uploads/" + filename
