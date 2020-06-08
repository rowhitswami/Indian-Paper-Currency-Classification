import os

# S3 Credentials
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
BUCKET = 'indian-currency-prediction'
REGION_HOST = 'ap-south-1'
UPLOAD_DIR = 'uploads/'
PRED_DIR = 'predictions/'

# Local Credentials
LABELS = ['10', '100', '20', '200', '2000', '50', '500']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'app/static/uploads/'
FLASK_SECRET_KEY = os.urandom(12).hex()
MODEL_PATH = 'app/model/model.h5'
WTF_CSRF_TIME_LIMIT = 1800