"""Utility functions for URL shortener service"""
from urllib.parse import urlparse
from pathlib import Path
import os

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Sequential counter starting at 2,383,280 (10 * 62^3) to generate codes starting with 'a'
# This module uses a file-backed counter so codes persist across process restarts.
INITIAL_COUNTER = 2383280
COUNTER_FILE = Path(__file__).resolve().parent.parent / ".counter"


def _load_counter() -> int:
    """Load the counter from `COUNTER_FILE`. Return `INITIAL_COUNTER` on error or if missing."""
    try:
        if COUNTER_FILE.exists():
            content = COUNTER_FILE.read_text().strip()
            if content:
                return int(content)
    except Exception:
        # best-effort: ignore errors and fall back to initial value
        pass
    return INITIAL_COUNTER


def _save_counter(value: int) -> None:
    """Atomically write the counter value to `COUNTER_FILE`. Best-effort, ignore failures."""
    try:
        tmp = COUNTER_FILE.with_suffix(".tmp")
        tmp.write_text(str(value))
        tmp.replace(COUNTER_FILE)
    except Exception:
        # don't raise — application should continue even if persistence fails
        pass


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
    current = _load_counter()
    code = encode_base62(current)
    _save_counter(current + 1)
    return code
