import os
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
LABELS = ['10', '100', '20', '200', '2000', '50', '500']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BUCKET = 'indian-currency-prediction'
UPLOAD_FOLDER = 'uploads/'
REGION_HOST = 'ap-south-1'
FLASK_SECRET_KEY = 'Sssshhhhh.....!!!!'