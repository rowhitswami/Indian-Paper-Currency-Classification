import os

# S3 Credentials
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
BUCKET = 'indian-currency-prediction'
REGION_HOST = 'ap-south-1'

# Local Credentials
LABELS = ['10', '100', '20', '200', '2000', '50', '500']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'app/static/uploads/'
FLASK_SECRET_KEY = 'Sssshhhhh.....!!!!'
MODEL_PATH = 'app/model/model.h5'