import numpy as np
from tiatoolbox.wsicore.wsireader import WSIReader

from app.utils.minio import load_wsi_from_minio, save_patch_to_minio
from app.models.schemas import WSIExtractPayload

def extract_patches(payload: WSIExtractPayload):
    """
    Extracts image patches from a Whole Slide Image (WSI) stored in MinIO.

    This function:
    - Downloads the WSI from MinIO using the provided object key.
    - Opens the WSI using TIA Toolbox.
    - Extracts patches at specified coordinates and resolution level.
    - Saves each patch back to MinIO with an appropriate naming convention.

    Args:
        payload (WSIExtractPayload): Parameters required for patch extraction.

    Returns:
        dict: A dictionary indicating success and containing saved patch paths in MinIO.
    """

    # Download the WSI from MinIO and get the local file path
    local_wsi_path = load_wsi_from_minio(payload.key)

    # Open the WSI using TIA Toolbox
    wsi = WSIReader.open(local_wsi_path)

    # Use provided coordinates or default to (0, 0)
    coords = payload.coordinates or [(0, 0)]
    saved_paths = []

    # Extract project and dataset identifiers from the object key
    parts = payload.key.split('/')
    project_id, dataset_id = parts[1], parts[2]
    base_filename = parts[-1]

    # Iterate over each coordinate and extract/save the patch
    for (x, y) in coords:
        # Read a patch from the WSI at the given location, resolution level, and size
        patch_pil = wsi.read_region(
            location=(x, y),
            size=(payload.patch_size, payload.patch_size),
            level=payload.level
        )

        # Convert the patch to a NumPy array
        patch_np = np.array(patch_pil)

        # Save the patch to MinIO and collect the returned path
        key = save_patch_to_minio(
            project_id, dataset_id, base_filename,
            patch_np, x, y, payload.output_format
        )
        saved_paths.append(key)

    # Return the result with saved patch paths
    return {"status": "success", "saved_patches": saved_paths}
