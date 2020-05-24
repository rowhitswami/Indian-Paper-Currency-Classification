import uuid
import boto3
import pickle
import datetime
from config import *
from PIL import Image
import tensorflow as tf
from keras.models import load_model
from keras.backend import set_session
from keras.preprocessing.image import img_to_array, load_img
global graph
global model

# Tensorflow config
config = tf.compat.v1.ConfigProto(device_count = {'GPU': 0})
sess = tf.compat.v1.Session(config=config)
graph = tf.compat.v1.get_default_graph()
set_session(sess)
model = load_model(MODEL_PATH)

def get_label(filename, file_path):
    global sess
    global graph
    processed_image = process_image(file_path)
    with graph.as_default():
        set_session(sess)
        classes = model.predict(processed_image)
    predicted_labels = classes.tolist()[0]
    saved_predictions = save_prediction_to_s3(filename, predicted_labels)
    if saved_predictions:
        label_classes = zip(LABELS, predicted_labels)
        max_label_class = sorted(label_classes, key = lambda t: t[1])[-1]
        max_label = max_label_class[0]
        return max_label, predicted_labels
    else:
        max_label = predicted_labels = None
        return max_label, predicted_labels

def process_image(file_path):
    img = load_img(file_path, target_size=(150,150))
    img = img_to_array(img)
    img = img.reshape(1,150,150,3).astype('float')
    img /= 255
    return img

def upload_file_to_s3(file_path, filename):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        compressed = compress_image(file_path)
        if compressed:
            with open(file_path, 'rb') as image:
                s3.upload_fileobj(image, BUCKET, UPLOAD_DIR + filename)
                return True
        else:
            return False
    except FileNotFoundError:
        return False

def save_prediction_to_s3(image_filename, predictions):
    filename = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [timestamp, UPLOAD_DIR + image_filename]
    data += predictions
    data = pickle.dumps(data)
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        s3.put_object(Body=data, Bucket=BUCKET, Key=PRED_DIR + filename)
        return True
    except:
        return False

def get_image_link(filename):
    return "https://" + BUCKET + ".s3." + REGION_HOST + ".amazonaws.com/uploads/" + filename

def compress_image(file_path):
    try:
        img = Image.open(file_path)
        img_width = img.size[0] * 20 // 100
        img_height = img.size[1] * 20 // 100
        img = img.resize((img_width,img_height),Image.ANTIALIAS)
        img.save(file_path, optimize=True,quality=50)
        return True
    except FileNotFoundError:
        return False

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS