from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterable

import botocore
from aiobotocore.config import AioConfig
from aiobotocore.session import AioBaseClient, get_session
from botocore.exceptions import ClientError


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
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AsyncIterable[AioBaseClient]:
        async with self.session.create_client(
            "s3", config=AioConfig(signature_version=botocore.UNSIGNED), **self.config
        ) as client:
            yield client

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

    async def get_url_for_file(
        self,
        object_name: str,
    ):
        try:
            async with self.get_client() as client:
                return await client.generate_presigned_url(
                    "get_object",
                    ExpiresIn=3600,
                    Params={"Bucket": self.bucket_name, "Key": object_name},
                )

        except ClientError as e:
            print(f"Error getting url: {e}")
