import boto3
import botocore

def download_s3_file(s3_url, local_filename=None, aws_access_key=None, aws_secret_key=None, region_name='us-east-1'):
    """
    Download a file from an S3 bucket URL with flexible authentication.
    
    Args:
        s3_url (str): Full S3 URL (e.g., 's3://bucket-name/path/to/file')
        local_filename (str, optional): Local path to save the file
        aws_access_key (str, optional): AWS Access Key ID
        aws_secret_key (str, optional): AWS Secret Access Key
        region_name (str, optional): AWS Region name
    
    Returns:
        str: Path of the downloaded file
    """
    # Parse S3 URL
    parts = s3_url.replace('s3://', '').split('/')
    bucket_name = parts[0]
    s3_key = '/'.join(parts[1:])
    
    # If no local filename is provided, use the S3 key filename
    if local_filename is None:
        local_filename = s3_key.split('/')[-1]
    
    # Create S3 client with flexible authentication
    try:
        if aws_access_key and aws_secret_key:
            # Explicit credentials
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region_name
            )
        else:
            # Default credential chain (AWS CLI, environment variables, IAM role)
            s3_client = boto3.client('s3', region_name=region_name)
        
        # Download the file
        s3_client.download_file(bucket_name, s3_key, local_filename)
        print(f"File downloaded successfully: {local_filename}")
        return local_filename
    
    except botocore.exceptions.ClientError as e:
        print(f"Error downloading file: {e}")
        raise
    except botocore.exceptions.NoCredentialsError:
        print("No AWS credentials found. Please configure credentials.")
        raise

# Example usage scenarios
try:
    # Method 1: Using default AWS credentials
    downloaded_file1 = download_s3_file('s3://your-bucket/path/to/file.txt')
    
    # Method 2: Providing explicit credentials
    downloaded_file2 = download_s3_file(
        's3://your-bucket/path/to/another-file.txt',
        aws_access_key='YOUR_ACCESS_KEY',
        aws_secret_key='YOUR_SECRET_KEY'
    )
except Exception as e:
    print(f"Download failed: {e}")
