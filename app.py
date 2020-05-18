from flask_cors import CORS
from flask import Flask, request, render_template, json, jsonify, send_from_directory
import json
import cv2
import numpy as np
import io
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
from keras.backend import set_session

app = Flask(__name__)
CORS(app)

config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )
sess = tf.Session(config=config)
global graph
graph = tf.get_default_graph()
set_session(sess)

global model
model = load_model('model/model.h5')

labels = ['10', '100', '20', '200', '2000', '50', '500']
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "12345678901"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def main():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        label = get_label('static/uploads/' + filename)
        flash('Image successfully uploaded and displayed')
        return render_template('index.html', filename=filename, prediction=label)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

def get_label(filename):
    processed_image = process_image(filename)
    print("\n\n\n\n\n\n*********** IMAGE SHAPE *************")
    print(processed_image.shape)
    print("\n\n\n\n\n\n")
    global sess
    global graph
    with graph.as_default():
        set_session(sess)
        classes = model.predict(processed_image)
    label_classes = zip(labels, classes.tolist()[0])
    label = sorted(label_classes, key = lambda t: t[1])[-1][0]
    return label

def process_image(filename):
    img = load_img(filename, target_size=(150,150))
    img = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    img = img.reshape(1,150,150,3).astype('float')
    img /= 255
    return img

if __name__ == "__main__":
    app.run(debug=True)
