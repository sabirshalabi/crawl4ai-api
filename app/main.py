from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import crawl, batch, extract

app = FastAPI(
    title="Crawl4AI API",
    description="A powerful web scraping API built with Crawl4AI and FastAPI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crawl.router, prefix="/api/v1", tags=["crawl"])
app.include_router(batch.router, prefix="/api/v1", tags=["batch"])
app.include_router(extract.router, prefix="/api/v1", tags=["extract"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Crawl4AI API is running"}
