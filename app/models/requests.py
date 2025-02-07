from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Literal
from enum import Enum

class ExtractionType(str, Enum):
    SUMMARY = "summary"
    QA = "qa"
    SCHEMA = "schema"

class BrowserAction(str, Enum):
    CLICK = "click"
    SCROLL = "scroll"
    WAIT = "wait"
    TYPE = "type"
    SUBMIT = "submit"

class WaitCondition(str, Enum):
    NETWORK_IDLE = "networkidle"
    LOAD = "load"
    DOM_CONTENT_LOADED = "domcontentloaded"

class Credentials(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None

class LLMConfig(BaseModel):
    provider: str = "openai"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 500

class RetryConfig(BaseModel):
    max_attempts: int = 3
    min_delay: float = 1.0
    max_delay: float = 10.0
    exponential: bool = True

class InteractionStep(BaseModel):
    action: BrowserAction
    selector: Optional[str] = None
    value: Optional[str] = None
    timeout: Optional[int] = 30000

class SessionConfig(BaseModel):
    auth_required: bool = False
    credentials: Optional[Credentials] = None
    interaction_steps: List[InteractionStep] = []
    wait_conditions: List[WaitCondition] = [WaitCondition.NETWORK_IDLE]
    timeout: int = 30000

class ExtractionConfig(BaseModel):
    extraction_type: ExtractionType
    custom_schema: Optional[Dict] = None
    llm_config: Optional[LLMConfig] = None

class BaseCrawlRequest(BaseModel):
    url: HttpUrl
    extract_images: bool = False
    extract_links: bool = False
    session_config: Optional[SessionConfig] = None

class BatchCrawlRequest(BaseModel):
    urls: List[HttpUrl]
    concurrent_limit: Optional[int] = 5
    retry_config: Optional[RetryConfig] = None
    extraction_config: Optional[ExtractionConfig] = None
    session_config: Optional[SessionConfig] = None

class ContentExtractionRequest(BaseCrawlRequest):
    extraction_config: ExtractionConfig
