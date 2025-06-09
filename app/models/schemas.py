from pydantic import BaseModel
from typing import Optional, List, Tuple, Union

class WSIExtractPayload(BaseModel):
    """
    Request payload schema for extracting patches from a Whole Slide Image (WSI).
    This schema defines the required and optional parameters for the extraction process.
    """

    key: str
    """MinIO object key for the WSI file."""

    patch_size: Union[int, Tuple[int, int]]
    """Size of the patches to extract, either as a single int (square) or (width, height) tuple."""

    save_prefix: Optional[str] = None
    """Optional prefix to be added to the saved patch filenames."""

    coordinates: Optional[List[Tuple[int, int]]] = None
    """List of (x, y) coordinates where patches should be extracted.
    If not provided, patches may be extracted across the entire slide or based on another logic.
    """

    level: Optional[int] = 0
    """Image pyramid level from which to extract patches. Default is 0 (highest resolution)."""

    output_format: Optional[str] = "png"
    """File format for output patches. Default is 'png'."""

    overwrite: Optional[bool] = False
    """Whether to overwrite existing patch files. Default is False."""

    return_minio_paths: Optional[bool] = True
    """If True, return the MinIO paths of the saved patches instead of local paths."""

    num_threads: Optional[int] = 1
    """Number of threads to use for parallel patch extraction. Default is 1."""
