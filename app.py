import boto3
from flask import Flask, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Get credentials from environment variables
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
BUCKET_NAME = 'my-unique-image-storage'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-west-1'
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            s3_client.upload_fileobj(file, BUCKET_NAME, filename)
            return {'message': 'File successfully uploaded'}, 200
        
        return {'error': 'File type not allowed'}, 400

    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
