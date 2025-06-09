import os
import io
import logging
from PIL import Image
import numpy as np
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.core.config import settings

# Initialize a MinIO (S3-compatible) client
s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
)

def load_wsi_from_minio(key: str) -> str:
    """
    Downloads a Whole Slide Image (WSI) file from MinIO and stores it temporarily on disk.

    Args:
        key (str): The MinIO object key of the WSI file.

    Returns:
        str: Local path where the WSI file is saved.

    Raises:
        HTTPException: If the file cannot be retrieved from MinIO.
    """
    try:
        # Retrieve the object from MinIO
        obj = s3.get_object(Bucket=settings.MINIO_BUCKET, Key=key)
        data = obj['Body'].read()

        # Save to a temporary file
        temp_path = f"/tmp/{os.path.basename(key)}"
        with open(temp_path, "wb") as f:
            f.write(data)

        return temp_path
    except ClientError as e:
        # Log and propagate error as HTTP 500
        logging.error(f"MinIO download error: {e}")
        raise HTTPException(status_code=500, detail=f"MinIO download error: {str(e)}")

def save_patch_to_minio(project_id, dataset_id, base_filename, patch_data, x, y, output_format):
    """
    Saves a given image patch to MinIO with a structured path.

    Args:
        project_id (str): Project identifier.
        dataset_id (str): Dataset identifier.
        base_filename (str): Base filename of the WSI.
        patch_data (np.ndarray): Image patch as a NumPy array.
        x (int): X-coordinate of the patch.
        y (int): Y-coordinate of the patch.
        output_format (str): File format to save the patch (e.g., "png", "jpeg").

    Returns:
        str: MinIO object key where the patch was saved.
    """
    # Convert the NumPy array to an image and save to buffer
    buffer = io.BytesIO()
    img = Image.fromarray(patch_data)
    img.save(buffer, format=output_format.upper())
    buffer.seek(0)

    # Construct object key
    base_name = os.path.splitext(os.path.basename(base_filename))[0]
    object_key = f"pending/{project_id}/{dataset_id}/{base_name}_x{x}_y{y}.{output_format}"

    # Upload the patch to MinIO
    s3.put_object(Bucket=settings.MINIO_BUCKET, Key=object_key, Body=buffer)
    return object_key
