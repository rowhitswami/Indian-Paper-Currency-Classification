import os
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
LABELS = ['10', '100', '20', '200', '2000', '50', '500']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BUCKET = 'indian-currency-prediction'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = 'uploads/'
TMP_FOLDER = '/app/static/tmp/'
REGION_HOST = 'ap-south-1'
FLASK_SECRET_KEY = 'Sssshhhhh.....!!!!'