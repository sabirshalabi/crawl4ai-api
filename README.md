# Crawl4AI API

A powerful and flexible web scraping API built with FastAPI and the Crawl4AI library. This API provides advanced web crawling capabilities with support for dynamic content, batch processing, and AI-powered content extraction.

## Features

- 🚀 **Single URL Crawling**: Extract content, images, and links from any webpage
- 📦 **Batch Processing**: Crawl multiple URLs concurrently with configurable limits
- 🤖 **AI-Powered Extraction**: Generate summaries and Q&A pairs from webpage content
- 🔄 **Dynamic Content Support**: Handle JavaScript-rendered pages and dynamic content
- 🎯 **Configurable Sessions**: Customize browser behavior and timeouts
- ⚡ **Asynchronous Processing**: Non-blocking operations for better performance

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd crawl4ai-api
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install --with-deps
   ```

3. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the API**
   - Interactive API docs: http://localhost:8000/docs
   - ReDoc documentation: http://localhost:8000/redoc

## Example Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/crawl",
    json={
        "url": "https://example.com",
        "extract_images": True,
        "extract_links": True
    }
)

print(response.json())
```

## API Endpoints

### GET /
Health check endpoint

### POST /api/v1/crawl
Crawl a webpage and return its content in markdown format.

Request body:
```json
{
    "url": "https://example.com",
    "extract_images": true,
    "extract_links": true
}
```

Response:
```json
{
    "url": "https://example.com",
    "markdown": "...",
    "images": ["..."],
    "links": ["..."]
}
```
