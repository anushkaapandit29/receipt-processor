import boto3
import os

def upload_file_to_s3(file_path, bucket_name="my-receipt-bucket-demo"):
    """Uploads a receipt image to an AWS S3 bucket."""
    # Note: In a real deployment, AWS credentials are handled via environment variables
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "YOUR_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "YOUR_SECRET_KEY"),
        region_name="us-east-1"
    )
    
    file_name = os.path.basename(file_path)
    try:
        s3_client.upload_file(file_path, bucket_name, file_name)
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        return s3_url
    except Exception as e:
        print(f"S3 Simulation/Upload Error: {e}")
        return None
