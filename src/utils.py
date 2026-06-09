"""Utility functions for URL shortener service"""
from urllib.parse import urlparse

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Sequential counter starting at 2,383,280 (10 * 62^3) to generate codes starting with 'a'
counter = 2383280


def validate_url(url: str) -> bool:
    """
    Validate if the provided URL is a valid HTTP/HTTPS URL
    
    Args:
        url: URL string to validate
        
    Returns:
        True if URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    
    if len(url) > 2048:
        return False
    
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.netloc:
            return False
        return True
    except Exception:
        return False


def encode_base62(num: int) -> str:
    """
    Convert a number to Base62 encoding
    
    Args:
        num: Number to encode
        
    Returns:
        Base62 encoded string
    """
    if num == 0:
        return BASE62_ALPHABET[0]
    
    encoded = ""
    while num > 0:
        encoded = BASE62_ALPHABET[num % 62] + encoded
        num //= 62
    
    return encoded


def generate_short_code() -> str:
    """
    Generate the next sequential short code using Base62 encoding
    Starts at counter 2,383,280 to generate codes beginning with 'a'
    
    Returns:
        A Base62 encoded short code
    """
    global counter
    code = encode_base62(counter)
    counter += 1
    return code
