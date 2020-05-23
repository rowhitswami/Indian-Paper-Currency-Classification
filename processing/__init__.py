from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import tensorflow as tf
from keras.backend import set_session
from config import ALLOWED_EXTENSIONS, LABELS, MODEL_PATH
global graph
global model

# Tensorflow config
config = tf.compat.v1.ConfigProto(device_count = {'GPU': 0})
sess = tf.compat.v1.Session(config=config)
graph = tf.compat.v1.get_default_graph()
set_session(sess)
model = load_model(MODEL_PATH)

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
    img = img_to_array(img)
    img = img.reshape(1,150,150,3).astype('float')
    img /= 255
    return img