import os
import numpy as np
from flask_cors import CORS
from processing import get_label, upload_file_to_s3, get_image_link
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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(file_path))
        uploaded = upload_file_to_s3(file_path, filename)
        if uploaded:
            image_url = get_image_link(filename)
            label = get_label(file_path)
            os.remove(file_path)
            return render_template('index.html', image_url=image_url, prediction=label)
        else:
            flash("Couldn't process and upload your image. Please try again!", 'alert-danger')
            return redirect(request.url)
    else:
        flash('Allowed image types are -> png, jpg, jpeg', 'alert-danger')
        return redirect(request.url)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS