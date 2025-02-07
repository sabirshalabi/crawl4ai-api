from fastapi import APIRouter, HTTPException
from app.models.requests import ContentExtractionRequest
from app.models.responses import ContentExtractionResponse
from app.services.extractor import ExtractorService

router = APIRouter()
extractor_service = ExtractorService()

@router.post("/extract", response_model=ContentExtractionResponse)
async def extract_content(request: ContentExtractionRequest):
    """
    Extract content from a URL using AI-powered extraction capabilities.
    Supports summarization, Q&A generation, and schema-based extraction.
    """
    try:
        return await extractor_service.extract_content(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
