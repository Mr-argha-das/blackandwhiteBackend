from boto3 import client
import os
import io
import uuid
def upload_image_to_space(file_content: bytes, filename: str):
    spaces_access_key = 'DO00AJFUXFALT4K6L69E'
    spaces_secret_key = 'kn2jUm8ox9W6fPQXvJ6E5kBtVZtzF5V5MvY6sJ8Cr8U'
    spaces_endpoint_url = 'https://blackwhite.blr1.digitaloceanspaces.com'
    spaces_bucket_name = 'BlackandWhite'

    # Generate a random filename using UUID
    # Generate a random filename using UUID
    random_filename = str(uuid.uuid4())
    file_extension = os.path.splitext(filename)[1]  # Extract file extension from the original filename

    random_filename_with_extension = f"{random_filename}{file_extension}"

    s3 = client('s3',
                 
                region_name='blr1',
                endpoint_url=spaces_endpoint_url,
                aws_access_key_id=spaces_access_key,
                aws_secret_access_key=spaces_secret_key, )

    # Create a BytesIO object to read file content from memory
    file_content_stream = io.BytesIO(file_content)

    s3.upload_fileobj(file_content_stream, spaces_bucket_name, random_filename_with_extension,  ExtraArgs={'ACL': 'public-read'})

    return f"{spaces_endpoint_url}/{spaces_bucket_name}/{random_filename_with_extension}"