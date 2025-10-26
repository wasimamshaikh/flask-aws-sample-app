import os
from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from botocore.exceptions import NoCredentialsError

# Configure Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages

# AWS S3 configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "dummy_key")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "dummy_secret")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "dummy-bucket")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Upload file page
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            try:
                s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file.filename)
                flash(f"File '{file.filename}' uploaded successfully!", "success")
                return redirect(url_for("list_files"))
            except NoCredentialsError:
                flash("AWS credentials not configured properly.", "danger")
        else:
            flash("No file selected.", "warning")
    return render_template("upload.html")

# List files in S3 bucket
@app.route("/files")
def list_files():
    try:
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        files = [obj["Key"] for obj in response.get("Contents", [])]
    except Exception as e:
        files = []
        flash(f"Failed to list files: {str(e)}", "danger")
    return render_template("list_files.html", files=files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


