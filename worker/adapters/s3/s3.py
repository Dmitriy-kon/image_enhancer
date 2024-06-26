from contextlib import asynccontextmanager

import botocore
from aiobotocore.session import get_session
from botocore.config import Config
from botocore.exceptions import ClientError
from config import config


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.signed_conf = Config(
            signature_version=botocore.UNSIGNED,
        )
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client(
            "s3", **self.config, config=self.signed_conf
        ) as client:
            yield client

    async def create_bucket_if_not_exists(self):
        try:
            async with self.get_client() as client:
                await client.create_bucket(Bucket=self.bucket_name)
                print(f"Bucket {self.bucket_name} created")
        except ClientError as e:
            print(f"Error creating bucket: {e}")

    async def upload_file(
        self,
        object_name: str,
        file: bytes,
    ):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )
                print(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_url_for_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                return await client.generate_presigned_url(
                    "get_object",
                    ExpiresIn=0,
                    Params={"Bucket": self.bucket_name, "Key": object_name},
                )
        except ClientError as e:
            print(f"Error getting url: {e}")


s3_storage_inner = S3Client(
    access_key=config.minio_config.access_key,
    secret_key=config.minio_config.secret_key,
    endpoint_url=config.minio_config.endpoint_url,
    bucket_name=config.minio_config.bucket_name,
)
