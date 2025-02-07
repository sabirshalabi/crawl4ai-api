from fastapi import APIRouter, HTTPException
from app.models.requests import BatchCrawlRequest
from app.models.responses import BatchCrawlResponse, JobStatus
from app.services.crawler import CrawlerService
from datetime import datetime
import uuid

router = APIRouter()
crawler_service = CrawlerService()
jobs = {}

@router.post("/crawl/batch", response_model=JobStatus)
async def start_batch_crawl(request: BatchCrawlRequest):
    """
    Start a batch crawling job for multiple URLs.
    Returns a job ID that can be used to check the status.
    """
    job_id = str(uuid.uuid4())
    
    # Create initial job status
    status = JobStatus(
        job_id=job_id,
        status="pending",
        progress=0.0,
        message="Job started"
    )
    jobs[job_id] = status
    
    try:
        # Start the crawling process
        result = await crawler_service.crawl_batch(request)
        
        # Update job status with results
        status.status = "completed"
        status.progress = 100.0
        status.message = f"Successfully crawled {len(result.successful_urls)} URLs"
        status.result = result.dict()
        status.updated_at = datetime.utcnow()
        
        return status
    except Exception as e:
        # Update job status with error
        status.status = "failed"
        status.message = str(e)
        status.updated_at = datetime.utcnow()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/crawl/batch/{job_id}", response_model=JobStatus)
async def get_batch_status(job_id: str):
    """
    Get the status of a batch crawling job.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status = jobs[job_id]
    if isinstance(status, JobStatus):
        return status
    
    # Handle legacy job format
    return JobStatus(
        job_id=job_id,
        status=status.get("status", "unknown"),
        progress=100.0 if status.get("status") == "completed" else 0.0,
        result=status.get("result"),
        message=status.get("error", "Processing")
    )
