"""Unit tests for URL shortener API"""
import pytest
from fastapi.testclient import TestClient
from src import main
from src.main import app, url_mapping


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    """Clear in-memory storage before each test"""
    url_mapping.clear()
    # Reset counter to initial value
    main.counter = 2383280
    yield
    url_mapping.clear()


def test_shorten_valid_url(client):
    """Test shortening a valid URL"""
    response = client.post("/shorten", json={"url": "https://example.com/very/long/url"})
    
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert "original_url" in data
    assert data["original_url"] == "https://example.com/very/long/url"
    # Code should start with 'a' and be at least 4 characters
    assert data["short_code"].startswith("a")
    assert len(data["short_code"]) >= 4


def test_shorten_invalid_url_no_scheme(client):
    """Test shortening URL without http/https scheme"""
    response = client.post("/shorten", json={"url": "example.com"})
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error"] == "invalid_url"


def test_shorten_invalid_url_ftp(client):
    """Test shortening URL with invalid scheme"""
    response = client.post("/shorten", json={"url": "ftp://example.com"})
    
    assert response.status_code == 400


def test_shorten_url_too_long(client):
    """Test shortening URL that exceeds max length"""
    long_url = "https://example.com/" + "a" * 2100
    response = client.post("/shorten", json={"url": long_url})
    
    assert response.status_code == 400


def test_redirect_valid_code(client):
    """Test redirecting with valid short code"""
    # Create a short URL
    create_response = client.post("/shorten", json={"url": "https://example.com"})
    short_code = create_response.json()["short_code"]
    
    # Verify code starts with 'a'
    assert short_code.startswith("a")
    
    # Redirect using the code
    response = client.get(f"/{short_code}", follow_redirects=False)
    
    assert response.status_code == 301
    assert response.headers["location"] == "https://example.com"


def test_redirect_invalid_code(client):
    """Test redirecting with invalid short code"""
    response = client.get("/invalid123")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]["error"] == "code_not_found"


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_multiple_urls_get_different_codes(client):
    """Test that different URLs get different codes"""
    response1 = client.post("/shorten", json={"url": "https://example.com/1"})
    response2 = client.post("/shorten", json={"url": "https://example.com/2"})
    
    code1 = response1.json()["short_code"]
    code2 = response2.json()["short_code"]
    
    # Both should start with 'a'
    assert code1.startswith("a")
    assert code2.startswith("a")
    # Codes should be sequential/different
    assert code1 != code2


def test_same_url_multiple_times_gets_different_codes(client):
    """Test that shortening same URL twice generates different codes"""
    response1 = client.post("/shorten", json={"url": "https://example.com"})
    response2 = client.post("/shorten", json={"url": "https://example.com"})
    
    code1 = response1.json()["short_code"]
    code2 = response2.json()["short_code"]
    
    # Both should start with 'a'
    assert code1.startswith("a")
    assert code2.startswith("a")
    # Codes should be different (sequential counter guarantees this)
    assert code1 != code2


def test_sequential_codes_are_ordered(client):
    """Test that codes are generated sequentially"""
    response1 = client.post("/shorten", json={"url": "https://example.com/1"})
    response2 = client.post("/shorten", json={"url": "https://example.com/2"})
    response3 = client.post("/shorten", json={"url": "https://example.com/3"})
    
    code1 = response1.json()["short_code"]
    code2 = response2.json()["short_code"]
    code3 = response3.json()["short_code"]
    
    # First code should be a000
    assert code1 == "a000"
    assert code2 == "a001"
    assert code3 == "a002"
