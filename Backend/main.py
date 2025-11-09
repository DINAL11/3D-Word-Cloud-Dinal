"""
FastAPI backend for 3D Word Cloud application.
Provides endpoints for article analysis and topic extraction.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any
import logging

from scraper import fetch_article
from analyzer import analyze_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="3D Word Cloud API",
    description="API for analyzing news articles and extracting topics for visualization",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class AnalyzeRequest(BaseModel):
    """Request model for article analysis."""
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.bbc.com/news/technology"
            }
        }


class WordData(BaseModel):
    """Model for individual word data."""
    word: str
    weight: float
    frequency: int


class AnalyzeResponse(BaseModel):
    """Response model for article analysis."""
    words: List[WordData]
    article_title: str
    word_count: int
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "words": [
                    {"word": "technology", "weight": 0.85, "frequency": 12},
                    {"word": "innovation", "weight": 0.72, "frequency": 8}
                ],
                "article_title": "Tech News Article",
                "word_count": 500,
                "url": "https://example.com/article"
            }
        }


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "3D Word Cloud API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze": "POST - Analyze an article URL",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "API is running"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_article(request: AnalyzeRequest):
    """
    Analyze an article URL and extract topics/keywords.
    
    Args:
        request: AnalyzeRequest containing the article URL
        
    Returns:
        AnalyzeResponse with word cloud data, title, and metadata
        
    Raises:
        HTTPException: If article cannot be fetched or analyzed
    """
    try:
        logger.info(f"Analyzing article: {request.url}")
        
        # Fetch article content
        article_data = fetch_article(request.url)
        
        if not article_data or not article_data.get("text"):
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the provided URL. The article may be behind a paywall or have a complex structure."
            )
        
        # Analyze text and extract keywords
        analysis_result = analyze_text(article_data["text"])
        
        if not analysis_result or not analysis_result.get("words"):
            raise HTTPException(
                status_code=500,
                detail="Text analysis failed. The article may not contain enough meaningful content."
            )
        
        # Prepare response
        response = AnalyzeResponse(
            words=[
                WordData(
                    word=word_data["word"],
                    weight=word_data["weight"],
                    frequency=word_data["frequency"]
                )
                for word_data in analysis_result["words"]
            ],
            article_title=article_data.get("title", "Untitled Article"),
            word_count=analysis_result.get("word_count", 0),
            url=request.url
        )
        
        logger.info(f"Successfully analyzed article. Found {len(response.words)} keywords.")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing article: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while analyzing the article: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
