# url-shortner

A simple, lightweight URL shortening service with basic APIs and in-memory storage.

## Features

- Shorten long URLs with auto-generated 6-character codes
- Redirect from short code to original URL
- In-memory storage (no database)
- Minimal dependencies
- Fast and simple API

## Tech Stack

- **Python** 3.8+
- **FastAPI** - Web framework
- In-memory dictionary for storage

## Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd url-shortne
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Run the Service

```bash
uvicorn src.main:app --reload
```

The service will start on `http://localhost:8000`

### Interactive API Documentation

FastAPI provides built-in interactive Swagger UI for testing APIs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc** (alternative): http://localhost:8000/redoc

Open `http://localhost:8000/docs` in your browser to test the endpoints directly!

## API Endpoints

### Using Swagger UI (Recommended)

1. Start the service: `uvicorn src.main:app --reload`
2. Open http://localhost:8000/docs in your browser
3. Click on any endpoint to expand it
4. Click "Try it out" button
5. Enter the required parameters and click "Execute"

### Manual Testing

#### POST /shorten
Create a short URL

**Request:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/url/path"}'
```

**Response (201):**
```json
{
  "short_code": "abc123",
  "original_url": "https://example.com/very/long/url/path"
}
```

**Error (400):**
```json
{
  "error": "invalid_url"
}
```

#### GET /{code}
Redirect to original URL

**Request:**
```bash
curl -L http://localhost:8000/abc123
```

**Response:** Redirects (301) to the original URL

**Error (404):**
```json
{
  "error": "code_not_found"
}
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

See [requirements.txt](requirements.txt) for full list.

## Development

### Running Tests

```bash
pytest
```

### Project Structure

```
url-shortner/
├── src/
│   ├── main.py              # FastAPI application and endpoints
│   └── utils.py             # Utility functions (e.g., URL validation, code generation)
├── tests/
│   └── test_main.py         # Unit tests
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── SRS.md                 # Service specification
```

## Notes

- All URLs are stored in memory and will be lost when the service restarts
- Maximum URL length: 2048 characters
- URLs must start with `http://` or `https://`
- Short codes are randomly generated 6-character alphanumeric strings

## License

MIT