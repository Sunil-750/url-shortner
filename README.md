# url-shortner

A simple, lightweight URL shortening service with basic APIs and MongoDB persistent storage.

## Features

- Shorten long URLs with auto-generated 6-character codes
- Redirect from short code to original URL
- Persistent MongoDB storage for data durability
- Minimal dependencies
- Fast and simple API

## Tech Stack

- **Python** 3.8+
- **FastAPI** - Web framework
- **MongoDB** - NoSQL database for persistent storage
- **PyMongo** - MongoDB Python driver

## Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd url-shortner
   ```

2. **Ensure MongoDB is running**
   ```bash
   # Using Docker (recommended)
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   
   # OR using local MongoDB installation
   mongod --dbpath /data/db
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure MongoDB connection (optional)**
   ```bash
   # Set custom MongoDB URI if needed (default: mongodb://127.0.0.1:27017/)
   export MONGODB_URI="mongodb://username:password@host:port/"
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

**Note**: You can generate short codes in Swagger UI, but to test the redirect functionality, copy the short code URL (e.g., `http://localhost:8000/abc123`) and paste it directly in your browser's address bar. This is due to browser CORS restrictions on cross-origin redirects.

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
│   ├── database.py          # MongoDB connection and CRUD operations
│   ├── utils.py             # Utility functions (e.g., URL validation, code generation)
│   └── __init__.py          # Package initialization
├── tests/
│   ├── test_main.py         # Unit tests
│   └── __init__.py          # Test package initialization
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── SRS.md                 # Service specification
```

## Notes

- All URLs are stored in MongoDB and persisted across service restarts
- Maximum URL length: 2048 characters
- URLs must start with `http://` or `https://`
- Short codes are randomly generated 6-character alphanumeric strings
- MongoDB unique index ensures no duplicate short codes
- Database name: `url_shortener`, Collection name: `urls`

## License

MIT