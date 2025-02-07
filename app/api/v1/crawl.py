from fastapi import APIRouter, HTTPException
from app.models.requests import BaseCrawlRequest
from app.models.responses import BaseCrawlResponse
from app.services.crawler import CrawlerService

router = APIRouter()
crawler_service = CrawlerService()

@router.post("/crawl", response_model=BaseCrawlResponse)
async def crawl_url(request: BaseCrawlRequest):
    """
    Crawl a single URL and return the content in markdown format.
    Optionally extract images and links from the page.
    """
    try:
        return await crawler_service.crawl_url(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
