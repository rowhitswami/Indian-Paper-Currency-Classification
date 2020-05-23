from flask_cors import CORS
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
from keras.backend import set_session
import os

LABELS = ['10', '100', '20', '200', '2000', '50', '500']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
MODEL = 'app/model/model.h5'
UPLOAD_FOLDER = 'app/static/uploads/'
FLASK_SECRET_KEY = 'Sssshhhhh.....!!!!'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

config = tf.compat.v1.ConfigProto(device_count = {'GPU': 0})
sess = tf.compat.v1.Session(config=config)

global graph
graph = tf.compat.v1.get_default_graph()
set_session(sess)

global model
model = load_model(MODEL)

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
        print("\n\n\n\n**************")
        print(BASE_DIR)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        label = get_label('app/static/uploads/' + filename)
        return render_template('index.html', filename=filename, prediction=label)
    else:
        flash('Allowed image types are -> png, jpg, jpeg', 'alert-danger')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

def get_label(filename):
    global sess
    global graph
    processed_image = process_image(filename)	
    with graph.as_default():	
        set_session(sess)
        classes = model.predict(processed_image)
    label_classes = zip(LABELS, classes.tolist()[0])
    max_label_class = sorted(label_classes, key = lambda t: t[1])[-1]
    label = max_label_class[0]
    return label
	
def process_image(filename):
    img = load_img(filename, target_size=(150,150))
    img = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    img = img.reshape(1,150,150,3).astype('float')
    img /= 255
    return img
