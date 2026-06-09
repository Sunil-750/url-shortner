"""FastAPI application for URL shortener service"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Dict
from urllib.parse import urlparse

from src.utils import generate_short_code

app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortening service with in-memory storage",
    version="1.0.0"
)

# In-memory storage
url_mapping: Dict[str, str] = {}


class ShortenRequest(BaseModel):
    """Request model for shortening a URL"""
    url: str


class ShortenResponse(BaseModel):
    """Response model for shortening a URL"""
    short_code: str
    original_url: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str


@app.post("/shorten", response_model=ShortenResponse, status_code=201)
def shorten_url(request: ShortenRequest) -> ShortenResponse:
    """
    Shorten a long URL
    
    Args:
        request: ShortenRequest containing the URL to shorten
        
    Returns:
        ShortenResponse with the generated short code and original URL
        
    Raises:
        HTTPException: 400 if URL is invalid
    """
    url = request.url.strip()
    
    # Validate URL
    if not url:
        raise HTTPException(status_code=400, detail={"error": "invalid_url"})
    
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("Invalid URL scheme")
        if not parsed.netloc:
            raise ValueError("Invalid URL")
        if len(url) > 2048:
            raise ValueError("URL too long")
    except Exception:
        raise HTTPException(status_code=400, detail={"error": "invalid_url"})
    
    # Generate short code using sequential counter with Base62 encoding
    short_code = generate_short_code()
    
    # Store mapping
    url_mapping[short_code] = url
    
    return ShortenResponse(short_code=short_code, original_url=url)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/{code}")
def redirect_to_url(code: str):
    """
    Redirect to the original URL using the short code
    
    Args:
        code: The short code to look up
        
    Returns:
        RedirectResponse to the original URL
        
    Raises:
        HTTPException: 404 if code is not found
    """
    if code not in url_mapping:
        raise HTTPException(status_code=404, detail={"error": "code_not_found"})
    
    original_url = url_mapping[code]
    return RedirectResponse(url=original_url, status_code=301)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
