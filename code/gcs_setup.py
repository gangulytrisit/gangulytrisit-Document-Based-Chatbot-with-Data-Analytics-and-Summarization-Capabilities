from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\IIT M DOCUMENTS\JOB\Figital Technologies\mcash-441605-5297063c9bfd.json"


client = storage.Client()
bucket_name = "my-document-storage-bucket"  
bucket = client.get_bucket(bucket_name)


def list_files_in_bucket(bucket):
    files = bucket.list_blobs()
    for file in files:
        print(f"Found file: {file.name}")


list_files_in_bucket(bucket)

