from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class CrawlMetadata(BaseModel):
    crawl_time: datetime
    content_type: Optional[str] = None
    status_code: int
    headers: Dict[str, str]
    final_url: HttpUrl

class ExtractedContent(BaseModel):
    summary: Optional[str] = None
    qa_pairs: Optional[List[Dict[str, str]]] = None
    structured_data: Optional[Dict[str, Any]] = None
    raw_text: Optional[str] = None

class URLError(BaseModel):
    url: HttpUrl
    error: str
    attempt_count: int
    last_attempt: datetime

class URLResult(BaseModel):
    url: HttpUrl
    markdown: str
    images: List[str] = []
    links: List[str] = []
    metadata: CrawlMetadata
    extracted_content: Optional[ExtractedContent] = None

class BatchMetadata(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    total_urls: int
    successful_count: int
    failed_count: int
    total_time_seconds: Optional[float] = None

class BaseCrawlResponse(BaseModel):
    url: HttpUrl
    markdown: str
    images: List[str] = []
    links: List[str] = []
    metadata: CrawlMetadata

class BatchCrawlResponse(BaseModel):
    successful_urls: List[URLResult]
    failed_urls: List[URLError]
    metadata: BatchMetadata

class ContentExtractionResponse(BaseCrawlResponse):
    extracted_content: ExtractedContent

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: float
    message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    result: Optional[Dict[str, Any]] = None
