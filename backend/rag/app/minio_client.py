
import io
import uuid
from datetime import timedelta
from typing import Optional
from minio import Minio
from minio.error import S3Error

class MinioStore:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, secure: bool, bucket: str, presign_days: int = 7):
        endpoint = endpoint.replace("http://", "").replace("https://", "")
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        self.bucket = bucket
        self.presign_days = presign_days
        self.ensure_bucket()

    def ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def put_bytes(self, key: str, data: bytes, content_type: Optional[str] = None):
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=key,
            data=io.BytesIO(data),
            length=len(data),
            content_type=content_type or "application/octet-stream",
        )

    def presigned_get(self, key: str) -> str:
        try:
            return self.client.presigned_get_object(self.bucket, key, expires=timedelta(days=self.presign_days))
        except S3Error:
            return f"s3://{self.bucket}/{key}"

    @staticmethod
    def build_object_key(user_id: str, session_id: str, ext: str) -> str:
        rid = uuid.uuid4().hex[:8]
        ext = (ext or "").lstrip(".") or "bin"
        return f"u/{user_id}/sess/{session_id}/{rid}.{ext}"
