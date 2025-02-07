from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from bs4 import BeautifulSoup
import asyncio
from typing import Optional

app = FastAPI(
    title="Crawl4AI API",
    description="A simple API for web crawling using Crawl4AI",
    version="0.1.0"
)

class CrawlRequest(BaseModel):
    url: HttpUrl
    extract_images: Optional[bool] = False
    extract_links: Optional[bool] = False

class CrawlResponse(BaseModel):
    url: str
    markdown: str
    images: list[str] = []
    links: list[str] = []

@app.get("/")
async def read_root():
    return {"status": "ok", "message": "Crawl4AI API is running"}

@app.post("/api/v1/crawl", response_model=CrawlResponse)
async def crawl_url(request: CrawlRequest):
    try:
        browser_conf = BrowserConfig(headless=True)
        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=1,
            page_timeout=30000,  # 30 seconds timeout
        )

        async with AsyncWebCrawler(config=browser_conf) as crawler:
            result = await crawler.arun(
                url=str(request.url),
                config=run_conf
            )

            # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(result.html, 'html.parser')

            # Extract images if requested
            images = []
            if request.extract_images:
                img_tags = soup.find_all('img')
                images = [img.get('src') for img in img_tags if img.get('src')]

            # Extract links if requested
            links = []
            if request.extract_links:
                link_tags = soup.find_all('a')
                links = [link.get('href') for link in link_tags if link.get('href')]

            return CrawlResponse(
                url=str(request.url),
                markdown=result.markdown,
                images=images,
                links=links
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
