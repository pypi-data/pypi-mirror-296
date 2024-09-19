import os
import uuid
from botocore.exceptions import NoCredentialsError
from boto3 import client
from boto3.s3.transfer import TransferConfig
from botocore.client import Config

from typing import Union, Optional
from pathlib import Path
from playwright.async_api import Download

from typing import TypedDict
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class UploadedFile:
    file_name: str
    bucket: str


class UploadFileToS3Configs(TypedDict):
    endpoint: Optional[str]
    fileNameOverride: Optional[str]


FileType = Union[Download, str, bytes]


async def upload_file_to_s3(
    file: FileType,
    endpoint: Optional[str] = None,
    fileNameOverride: Optional[str] = None,
) -> UploadedFile:
    is_downloaded_file = isinstance(file, Download)

    if is_downloaded_file and not await file.path():
        raise ValueError("File path not found")

    region_name = os.environ.get("INTUNED_S3_REGION")
    aws_access_key_id = os.environ.get("INTUNED_S3_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("INTUNED_S3_SECRET_ACCESS_KEY")

    s3_client = client(
        "s3",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint,
    )

    file_body = await get_file_body(file)
    suggested_file_name = file.suggested_filename if is_downloaded_file else None

    file_name = (
        fileNameOverride
        if fileNameOverride is not None
        else suggested_file_name or str(uuid.uuid4())
    )

    bucket_name = os.environ.get("INTUNED_S3_BUCKET")

    try:
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_body,
        )
    except NoCredentialsError:
        raise Exception("Credentials not available")

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return UploadedFile(
            file_name,
            bucket_name,
        )
    else:
        raise Exception("Error uploading file")


async def get_file_body(file: FileType):
    if isinstance(file, Download):
        file_path = await file.path()
        if not file_path:
            raise ValueError("Downloaded file path not found")
        with open(file_path, "rb") as f:
            return f.read()
    return file
