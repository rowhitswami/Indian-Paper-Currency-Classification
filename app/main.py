import os
import numpy as np
from flask_cors import CORS
from processing import get_label
from werkzeug.utils import secure_filename
from config import FLASK_SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from flask import Flask, flash, request, redirect, url_for, render_template

# Flask config
app = Flask(__name__)
CORS(app)
app.secret_key = FLASK_SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        label = get_label('app/static/uploads/' + filename)
        return render_template('index.html', filename=filename, prediction=label)
    else:
        flash('Allowed image types are -> png, jpg, jpeg', 'alert-danger')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS