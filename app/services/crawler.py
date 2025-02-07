from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

from app.models.requests import (
    BaseCrawlRequest, BatchCrawlRequest, SessionConfig,
    RetryConfig, ContentExtractionRequest
)
from app.models.responses import (
    BaseCrawlResponse, BatchCrawlResponse, URLResult,
    URLError, CrawlMetadata, BatchMetadata
)

class CrawlerService:
    def __init__(self):
        self.browser_config = BrowserConfig(headless=True)
        
    async def _create_metadata(self, result: Any, url: str) -> CrawlMetadata:
        """Create metadata from crawl result"""
        return CrawlMetadata(
            crawl_time=datetime.utcnow(),
            content_type=result.content_type if hasattr(result, 'content_type') else None,
            status_code=result.status_code if hasattr(result, 'status_code') else 200,
            headers=result.headers if hasattr(result, 'headers') else {},
            final_url=url
        )

    def _extract_from_html(self, html: str, extract_images: bool = False, extract_links: bool = False) -> Tuple[List[str], List[str]]:
        """Extract images and links from HTML content"""
        soup = BeautifulSoup(html, 'html.parser')
        
        images = []
        if extract_images:
            img_tags = soup.find_all('img')
            images = [img.get('src') for img in img_tags if img.get('src')]

        links = []
        if extract_links:
            link_tags = soup.find_all('a')
            links = [link.get('href') for link in link_tags if link.get('href')]

        return images, links

    async def _configure_session(self, crawler: AsyncWebCrawler, config: SessionConfig) -> None:
        """Configure browser session based on session config"""
        if config.auth_required and config.credentials:
            # Implementation for authentication will go here
            pass

        for step in config.interaction_steps:
            # Implementation for browser interactions will go here
            pass

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def crawl_url(self, request: BaseCrawlRequest) -> BaseCrawlResponse:
        """Crawl a single URL with retry logic"""
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=1,
            page_timeout=request.session_config.timeout if request.session_config else 30000,
        )

        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            if request.session_config:
                await self._configure_session(crawler, request.session_config)

            result = await crawler.arun(
                url=str(request.url),
                config=run_config
            )

            images, links = self._extract_from_html(
                result.html,
                request.extract_images,
                request.extract_links
            )

            metadata = await self._create_metadata(result, str(request.url))

            return BaseCrawlResponse(
                url=request.url,
                markdown=result.markdown,
                images=images,
                links=links,
                metadata=metadata
            )

    async def crawl_batch(self, request: BatchCrawlRequest) -> BatchCrawlResponse:
        """Crawl multiple URLs concurrently"""
        start_time = datetime.utcnow()
        successful_urls: List[URLResult] = []
        failed_urls: List[URLError] = []

        semaphore = asyncio.Semaphore(request.concurrent_limit or 5)
        
        async def crawl_with_semaphore(url: str) -> None:
            async with semaphore:
                try:
                    single_request = BaseCrawlRequest(
                        url=url,
                        extract_images=True,
                        extract_links=True,
                        session_config=request.session_config
                    )
                    result = await self.crawl_url(single_request)
                    successful_urls.append(URLResult(
                        url=url,
                        markdown=result.markdown,
                        images=result.images,
                        links=result.links,
                        metadata=result.metadata
                    ))
                except Exception as e:
                    failed_urls.append(URLError(
                        url=url,
                        error=str(e),
                        attempt_count=1,
                        last_attempt=datetime.utcnow()
                    ))

        tasks = [crawl_with_semaphore(url) for url in request.urls]
        await asyncio.gather(*tasks)

        end_time = datetime.utcnow()
        
        return BatchCrawlResponse(
            successful_urls=successful_urls,
            failed_urls=failed_urls,
            metadata=BatchMetadata(
                start_time=start_time,
                end_time=end_time,
                total_urls=len(request.urls),
                successful_count=len(successful_urls),
                failed_count=len(failed_urls),
                total_time_seconds=(end_time - start_time).total_seconds()
            )
        )
