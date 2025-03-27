import json
import firebase_admin
from firebase_admin import credentials, storage
from fastapi import UploadFile
import logging
import os
from google.cloud import storage as gcs
from typing import Any
from dotenv import load_dotenv

load_dotenv()

firebase_secret_key = os.getenv("FIREBASE_SECRET_KEY")
bucket_name = os.getenv("FIREBASE_BUCKET_NAME")


class FirebaseClient:
    def __init__(self):
        self.bucket_name = bucket_name
        self.logger = logging.getLogger("FirebaseClient")
        self.logger.setLevel(logging.INFO)

        try:
            self.logger.info("Connecting to Firebase...")
            firebase_cred = json.loads(firebase_secret_key)
            cred = credentials.Certificate(firebase_cred)
            firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})
            self.bucket = storage.bucket()
            self.logger.info("Firebase connection OK")
        except Exception as e:
            self.logger.error(f"Firebase connection KO: {str(e)}")
            raise

    def upload_file(
        self, file: UploadFile, file_name_with_directories_path: str
    ) -> None:
        """Upload a file to Firebase Storage."""
        blob = self.bucket.blob(file_name_with_directories_path)
        blob.upload_from_file(file.file, content_type=file.content_type)

    def upload_file_and_get_public_url(
        self, file: UploadFile, file_name_with_directories_path: str
    ) -> str:
        """Upload a file and return its public URL."""
        blob = self.bucket.blob(file_name_with_directories_path)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()
        return f"https://storage.googleapis.com/{self.bucket_name}/{file_name_with_directories_path}"

    def upload_json(self, file_name_with_directories_path: str, json_data: Any) -> str:
        """Upload a JSON object to Firebase Storage."""
        json_string = json.dumps(json_data, indent=2)
        blob = self.bucket.blob(file_name_with_directories_path)
        blob.upload_from_string(json_string, content_type="application/json")
        return f"https://storage.googleapis.com/{self.bucket_name}/{file_name_with_directories_path}"

    def download_file(self, file_name_with_directories_path: str) -> bytes:
        """Download a file from Firebase Storage."""
        blob = self.bucket.blob(file_name_with_directories_path)
        return blob.download_as_bytes()

    def delete_files(self, directory_path: str) -> None:
        """Delete all files in the specified directory."""
        blobs = self.bucket.list_blobs(prefix=directory_path)
        for blob in blobs:
            blob.delete()


firebase_client = FirebaseClient()
