---

### **1. Create an S3 Bucket**
1. Used the AWS CLI to create a unique bucket:
   ```bash
   aws s3api create-bucket --bucket my-unique-image-storage --region us-west-1 --create-bucket-configuration LocationConstraint=us-west-1
   ```

2. Verified the bucket creation:
   ```bash
   aws s3 ls
   ```

---

### **2. Set Up Bucket Policy**
1. Created a bucket policy file (`bucket-policy.json`) to allow the IAM user access:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::ACCOUNT_ID:user/s3-user"
               },
               "Action": "s3:*",
               "Resource": [
                   "arn:aws:s3:::my-unique-image-storage",
                   "arn:aws:s3:::my-unique-image-storage/*"
               ]
           }
       ]
   }
   ```

2. Applied the bucket policy:
   ```bash
   aws s3api put-bucket-policy --bucket my-unique-image-storage --policy file://bucket-policy.json
   ```

---

### **3. Create an IAM User**
1. Created an IAM user (`s3-user`) with **Programmatic Access**.
2. Attached an inline policy allowing access to the bucket:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": "s3:*",
               "Resource": [
                   "arn:aws:s3:::my-unique-image-storage",
                   "arn:aws:s3:::my-unique-image-storage/*"
               ]
           }
       ]
   }
   ```

3. Saved the **Access Key** and **Secret Key** for the IAM user.

---

### **4. Set Up Flask Application**
1. Installed required Python libraries:
   ```bash
   pip install boto3 flask
   ```

2. Wrote a Flask application (`app.py`) to handle file uploads:
   ```python
   import boto3
   from flask import Flask, request
   from werkzeug.utils import secure_filename
   import os

   app = Flask(__name__)

   # Environment variables for AWS credentials
   AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
   AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
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
   ```

3. Exported the AWS credentials as environment variables:
   ```bash
   export AWS_ACCESS_KEY=YOUR_ACCESS_KEY
   export AWS_SECRET_KEY=YOUR_SECRET_KEY
   ```

4. Ran the Flask application:
   ```bash
   python app.py
   ```

---

### **5. Test File Upload**
1. Placed a test file (`table.jpeg`) in the same directory as `app.py`.
2. Used `curl` to test the Flask endpoint:
   ```bash
   curl -X POST -F "file=@table.jpeg" http://127.0.0.1:5000/upload
   ```

---

### **6. Verify File Upload**
1. Checked the S3 bucket using the AWS CLI:
   ```bash
   aws s3 ls s3://my-unique-image-storage/ --profile s3-user
   ```

2. Confirmed that the uploaded file (`table.jpeg`) exists in the bucket.

---

### **Outcome**
- Successfully uploaded files to S3 using Flask.
- Verified file existence in the S3 bucket using the AWS CLI.

---
