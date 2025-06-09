import os

class Settings:
    """
    Application configuration settings for connecting to the MinIO object storage.

    Environment variables can be used to override the default values.
    These settings are used throughout the application for file storage operations.
    """

    # The MinIO server endpoint (host:port)
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "minio:9000")

    # Access key for authenticating with MinIO
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")

    # Secret key for authenticating with MinIO
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")

    # Default bucket name used in MinIO for storing data
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "automicro")

# Instantiate settings to be used across the application
settings = Settings()
