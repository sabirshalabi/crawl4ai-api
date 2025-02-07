# Crawl4AI API Documentation

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
  - [Single URL Crawling](#single-url-crawling)
  - [Batch Processing](#batch-processing)
  - [AI Content Extraction](#ai-content-extraction)
- [Advanced Usage](#advanced-usage)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Performance Optimization](#performance-optimization)

## Overview

Crawl4AI API is a high-performance web scraping solution that combines the power of FastAPI, Playwright, and AI capabilities. It provides three main functionalities:

1. **Single URL Crawling**: Extract content from individual webpages
2. **Batch Processing**: Handle multiple URLs concurrently
3. **AI-Powered Analysis**: Generate summaries and insights from webpage content

## Getting Started

### Installation

1. Clone the repository and create a virtual environment:
   ```bash
   git clone <repository-url>
   cd crawl4ai-api
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install --with-deps
   ```

3. Configure environment variables (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

### Configuration

Key configuration options:

```python
# config.py
Settings = {
    "MAX_CONCURRENT_CRAWLS": 5,
    "DEFAULT_TIMEOUT": 30000,
    "RATE_LIMIT": {
        "calls": 60,
        "period": 60
    },
    "RETRY_CONFIG": {
        "max_attempts": 3,
        "min_delay": 1.0,
        "max_delay": 5.0
    }
}
```

## API Endpoints

### Single URL Crawling

**Endpoint**: `POST /api/v1/crawl`

**Purpose**: Crawl a single webpage and extract specified content.

**Request Format**:
```json
{
    "url": "https://example.com",
    "extract_images": true,
    "extract_links": true,
    "session_config": {
        "wait_conditions": ["networkidle", "load"],
        "timeout": 30000,
        "viewport": {
            "width": 1920,
            "height": 1080
        },
        "user_agent": "Custom User Agent String"
    }
}
```

**Response Format**:
```json
{
    "url": "https://example.com",
    "markdown": "Extracted content in markdown format",
    "images": [
        {
            "url": "image1.jpg",
            "alt": "Image description",
            "dimensions": {
                "width": 800,
                "height": 600
            }
        }
    ],
    "links": [
        {
            "url": "https://example.com/page1",
            "text": "Link text",
            "is_internal": true
        }
    ],
    "metadata": {
        "title": "Page Title",
        "description": "Meta description",
        "language": "en",
        "last_modified": "2024-02-06T23:43:18-05:00"
    }
}
```

### Batch Processing

**Endpoint**: `POST /api/v1/crawl/batch`

**Purpose**: Process multiple URLs concurrently with advanced configuration.

**Request Format**:
```json
{
    "urls": [
        "https://example1.com",
        "https://example2.com"
    ],
    "concurrent_limit": 2,
    "retry_config": {
        "max_attempts": 3,
        "min_delay": 1.0,
        "max_delay": 5.0
    },
    "session_config": {
        "wait_conditions": ["networkidle"],
        "timeout": 30000
    }
}
```

**Initial Response**:
```json
{
    "job_id": "uuid-string",
    "status": "pending",
    "progress": 0.0,
    "message": "Job started"
}
```

**Status Check Endpoint**: `GET /api/v1/crawl/batch/{job_id}`

**Status Response**:
```json
{
    "job_id": "uuid-string",
    "status": "completed",
    "progress": 100.0,
    "message": "Successfully crawled 2 URLs",
    "result": {
        "successful_urls": ["url1", "url2"],
        "failed_urls": [],
        "results": {
            "url1": { /* crawl result */ },
            "url2": { /* crawl result */ }
        },
        "stats": {
            "total_time": 5.2,
            "average_time_per_url": 2.6
        }
    }
}
```

### AI Content Extraction

**Endpoint**: `POST /api/v1/extract`

**Purpose**: Extract and analyze content using AI capabilities.

**Request Format**:
```json
{
    "url": "https://example.com",
    "extraction_config": {
        "extraction_type": "summary",
        "llm_config": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        },
        "options": {
            "max_length": 500,
            "focus_elements": ["article", "main"],
            "exclude_elements": ["nav", "footer"]
        }
    }
}
```

**Response Format**:
```json
{
    "url": "https://example.com",
    "extraction_type": "summary",
    "content": {
        "summary": "Generated summary text",
        "key_points": [
            "Main point 1",
            "Main point 2"
        ],
        "metadata": {
            "word_count": 150,
            "processing_time": 2.5,
            "confidence_score": 0.95
        }
    }
}
```

## Advanced Usage

### Session Configuration

Customize browser behavior:
```python
session_config = {
    "wait_conditions": [
        "networkidle",    # Wait for network to be idle
        "load",          # Wait for load event
        "domcontentloaded"  # Wait for DOM content
    ],
    "timeout": 30000,   # 30 seconds
    "viewport": {
        "width": 1920,
        "height": 1080
    },
    "user_agent": "Custom User Agent String",
    "headers": {
        "Custom-Header": "Value"
    },
    "cookies": [
        {
            "name": "session",
            "value": "xyz",
            "domain": "example.com"
        }
    ]
}
```

### Retry Configuration

Handle transient failures:
```python
retry_config = {
    "max_attempts": 3,     # Maximum retry attempts
    "min_delay": 1.0,      # Minimum delay between retries
    "max_delay": 5.0,      # Maximum delay between retries
    "exponential": True,   # Use exponential backoff
    "retry_on": [         # HTTP status codes to retry on
        429,  # Too Many Requests
        503,  # Service Unavailable
        504   # Gateway Timeout
    ]
}
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Successful request
- 400: Bad request (invalid parameters)
- 401: Unauthorized
- 404: Resource not found
- 429: Too many requests
- 500: Server error
- 503: Service unavailable

Error Response Format:
```json
{
    "detail": "Detailed error message",
    "error_code": "ERROR_CODE",
    "timestamp": "2024-02-06T23:43:18-05:00",
    "request_id": "uuid-string",
    "additional_info": {
        "failed_validation": ["field1", "field2"],
        "suggestion": "How to fix the error"
    }
}
```

## Best Practices

1. **Rate Limiting**
   - Respect website's robots.txt
   - Implement reasonable delays between requests
   - Use batch processing for multiple URLs

2. **Error Handling**
   - Implement proper retry logic
   - Log errors for debugging
   - Handle timeouts gracefully

3. **Resource Management**
   - Monitor memory usage
   - Clean up browser instances
   - Use connection pooling

4. **Performance Optimization**
   - Cache frequently accessed content
   - Use appropriate timeouts
   - Optimize concurrent processing

## Performance Optimization

1. **Caching Strategy**
   ```python
   cache_config = {
       "ttl": 3600,           # Cache TTL in seconds
       "max_size": 1000,     # Maximum cache entries
       "strategy": "lru"     # Least Recently Used
   }
   ```

2. **Resource Limits**
   ```python
   resource_limits = {
       "max_memory": "1G",
       "max_cpu": 2,
       "max_browser_instances": 5
   }
   ```

3. **Monitoring Metrics**
   - Request latency
   - Success/failure rates
   - Resource utilization
   - Cache hit rates

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Endpoints](#endpoints)
  - [Single URL Crawling](#single-url-crawling)
  - [Batch Processing](#batch-processing)
  - [AI Content Extraction](#ai-content-extraction)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Overview

The Crawl4AI API provides three main functionalities:
1. Single URL crawling with customizable extraction
2. Batch URL processing with concurrent execution
3. AI-powered content extraction and analysis

## Authentication

Currently, the API operates without authentication. For production use, it's recommended to implement an authentication mechanism.

## Rate Limiting

Default rate limits:
- 60 requests per minute for single URL crawling
- 30 requests per minute for batch processing
- 20 requests per minute for AI extraction

## Endpoints

### Single URL Crawling

**Endpoint**: `POST /api/v1/crawl`

Crawls a single URL and extracts specified content.

**Request Body**:
```json
{
    "url": "https://example.com",
    "extract_images": true,
    "extract_links": true,
    "session_config": {
        "wait_conditions": ["networkidle", "load", "domcontentloaded"],
        "timeout": 30000,
        "viewport": {
            "width": 1920,
            "height": 1080
        }
    }
}
```

**Parameters**:
- `url` (required): Target URL to crawl
- `extract_images` (optional): Extract image URLs (default: false)
- `extract_links` (optional): Extract hyperlinks (default: false)
- `session_config` (optional): Browser session configuration
  - `wait_conditions`: List of conditions to wait for
  - `timeout`: Maximum wait time in milliseconds
  - `viewport`: Browser viewport settings

**Response**:
```json
{
    "url": "https://example.com",
    "markdown": "Extracted content in markdown format",
    "images": ["image1.jpg", "image2.jpg"],
    "links": ["link1.html", "link2.html"],
    "metadata": {
        "title": "Page Title",
        "description": "Meta description",
        "language": "en"
    }
}
```

### Batch Processing

**Endpoint**: `POST /api/v1/crawl/batch`

Processes multiple URLs concurrently.

**Request Body**:
```json
{
    "urls": [
        "https://example1.com",
        "https://example2.com"
    ],
    "concurrent_limit": 2,
    "retry_config": {
        "max_attempts": 3,
        "min_delay": 1.0,
        "max_delay": 5.0
    }
}
```

**Parameters**:
- `urls` (required): List of URLs to process
- `concurrent_limit` (optional): Maximum concurrent requests (default: 3)
- `retry_config` (optional): Retry configuration for failed requests
  - `max_attempts`: Maximum retry attempts
  - `min_delay`: Minimum delay between retries in seconds
  - `max_delay`: Maximum delay between retries in seconds

**Response**:
```json
{
    "job_id": "uuid-string",
    "status": "pending",
    "progress": 0.0,
    "message": "Job started"
}
```

**Job Status Endpoint**: `GET /api/v1/crawl/batch/{job_id}`

**Response**:
```json
{
    "job_id": "uuid-string",
    "status": "completed",
    "progress": 100.0,
    "message": "Successfully crawled 2 URLs",
    "result": {
        "successful_urls": ["url1", "url2"],
        "failed_urls": [],
        "results": {
            "url1": { /* crawl result */ },
            "url2": { /* crawl result */ }
        }
    }
}
```

### AI Content Extraction

**Endpoint**: `POST /api/v1/extract`

Extracts and analyzes content using AI capabilities.

**Request Body**:
```json
{
    "url": "https://example.com",
    "extraction_config": {
        "extraction_type": "summary",
        "llm_config": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }
    }
}
```

**Parameters**:
- `url` (required): Target URL for extraction
- `extraction_config` (required): Configuration for AI extraction
  - `extraction_type`: Type of extraction ("summary" or "qa")
  - `llm_config`: Language model configuration
    - `provider`: AI provider (e.g., "openai")
    - `model`: Model name
    - `temperature`: Creativity parameter (0.0-1.0)

**Response**:
```json
{
    "url": "https://example.com",
    "extraction_type": "summary",
    "content": {
        "summary": "Generated summary text",
        "key_points": ["point1", "point2"],
        "metadata": {
            "word_count": 150,
            "processing_time": 2.5
        }
    }
}
```

## Configuration

### Session Configuration Options
```python
session_config = {
    "wait_conditions": [
        "networkidle",  # Wait for network to be idle
        "load",         # Wait for load event
        "domcontentloaded"  # Wait for DOM content
    ],
    "timeout": 30000,  # 30 seconds
    "viewport": {
        "width": 1920,
        "height": 1080
    },
    "user_agent": "Custom User Agent String",
    "headers": {
        "Custom-Header": "Value"
    }
}
```

### Retry Configuration Options
```python
retry_config = {
    "max_attempts": 3,    # Maximum retry attempts
    "min_delay": 1.0,     # Minimum delay between retries
    "max_delay": 5.0,     # Maximum delay between retries
    "exponential": True   # Use exponential backoff
}
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Successful request
- 400: Bad request (invalid parameters)
- 404: Resource not found
- 429: Too many requests
- 500: Server error

Error Response Format:
```json
{
    "detail": "Error message",
    "error_code": "ERROR_CODE",
    "timestamp": "2024-02-06T23:41:01-05:00"
}
```

## Best Practices

1. **Rate Limiting**:
   - Respect rate limits to avoid being blocked
   - Implement exponential backoff for retries

2. **Resource Management**:
   - Use batch processing for multiple URLs
   - Set appropriate timeouts
   - Monitor memory usage

3. **Error Handling**:
   - Always check response status codes
   - Implement proper error handling
   - Log errors for debugging

4. **Performance**:
   - Use concurrent processing when appropriate
   - Cache frequently accessed content
   - Monitor response times

5. **Ethical Crawling**:
   - Respect robots.txt
   - Implement reasonable delays
   - Don't overload servers
