import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import WSIExtractPayload
from app.services.extractor import extract_patches

# Create an API router instance
router = APIRouter()

@router.post("/patch-extract")
async def patch_extract(payload: WSIExtractPayload):
    """
    Endpoint for extracting image patches from a Whole Slide Image (WSI).

    Receives a payload with WSI details and patch coordinates,
    and returns the result of the extraction process.

    Args:
        payload (WSIExtractPayload): Data class containing the necessary
                                     parameters for patch extraction.

    Returns:
        dict: Result or status message from the patch extraction service.

    Raises:
        HTTPException: If an unexpected error occurs during extraction.
    """
    try:
        # Call the core extraction service with the provided payload
        return extract_patches(payload)
    except Exception as e:
        # Log the error and return a 500 response
        logging.error(f"Patch extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
