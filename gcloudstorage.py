
# import packages
from google.cloud import storage
from dotenv import load_dotenv
from datetime import datetime

# load env vars
load_dotenv()


# define function that uploads a file from the bucket
def upload_cs_file(bucket_name, source_file_name, destination_file_name): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)

    return True

# define function that downloads a file from the bucket
def download_cs_file(bucket_name, file_name, destination_file_name): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True

# define function that list files in the bucket
def list_cs_files(bucket_name): 
    storage_client = storage.Client()

    file_list = storage_client.list_blobs(bucket_name)
    file_list = [file.name for file in file_list]

    return file_list

# define function that generates the public URL, default expiration is set to 24 hours
def get_cs_file_url(bucket_name, file_name, expire_in=datetime.today() + datetime.timedelta(10000)): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    url = bucket.blob(file_name).generate_signed_url(expire_in)

    return url

def upload_blob_from_stream(bucket_name, file_obj, destination_blob_name):
    """Uploads bytes from a stream or other file-like object to a blob."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The stream or file (file-like object) from which to read
    # import io
    # file_obj = io.BytesIO()
    # file_obj.write(b"This is test data.")

    # The desired name of the uploaded GCS object (blob)
    # destination_blob_name = "storage-object-name"

    # Construct a client-side representation of the blob.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Rewind the stream to the beginning. This step can be omitted if the input
    # stream will always be at a correct position.
    file_obj.seek(0)

    # Upload data from the stream to your bucket.
    blob.upload_from_file(file_obj)

    # print(
    #     f"Stream data uploaded to {destination_blob_name} in bucket {bucket_name}."
    # )

    return True

