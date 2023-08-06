import os
from dotenv import load_dotenv

load_dotenv()

# S3 Credentials
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
BUCKET = os.environ.get("ICP_BUCKET")
REGION_HOST = os.environ.get("ICP_BUCKET_REGION")
UPLOAD_DIR = os.environ.get("ICP_UPLOAD_DIR")
PRED_DIR = os.environ.get("ICP_PRED_DIR")

# Local Credentials
LABELS = ['10', '100', '20', '200', '2000', '50', '500']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'app/static/uploads/'
FLASK_SECRET_KEY = os.environ.get("ICP_FLASK_SECRET_KEY")
MODEL_PATH = 'app/model/model.h5'
WTF_CSRF_TIME_LIMIT = 1800
SENTRY_INIT= os.environ.get("SENTRY_INIT")