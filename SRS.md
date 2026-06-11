**Basic URL Shortener Service — SRS**

Project: Basic URL Shortener
Objective: Simple API to shorten long URLs and retrieve them using generated short codes. MongoDB persistent storage.

Purpose
- Provide a minimal specification for a basic URL shortening service with simple API endpoints and persistent MongoDB storage.

Scope
- In-scope: `POST /shorten`, `GET /{code}`, MongoDB database for persistent storage, URL validation.
- Out-of-scope: custom aliases, authentication, rate limiting, analytics, caching layers, scalability optimization.

Key Definitions
- Short code: generated URL-safe identifier (e.g., `abc123`).
- In-memory storage: dictionary/hash map stored in application memory.

API Endpoints

**POST /shorten**
- Request: `{ "url": "https://example.com/very/long/url" }`
- Validate: URL must start with `http://` or `https://`; max length 2048 characters.
- Generate: Random 6-character alphanumeric code.
- Response (201):
  ```json
  {
    "short_code": "abc123",
    "original_url": "https://example.com/very/long/url"
  }
  ```
- Error (400): `{ "error": "invalid_url" }` if URL is invalid.

**GET /{code}**
- If code exists: Redirect (301) to original URL.
- If code not found (404): `{ "error": "code_not_found" }`

Data Model
- Datastore: MongoDB document database
  - Collection: `urls`
  - Document Schema:
    ```json
    {
      "short_code": "abc123",
      "original_url": "https://example.com/very/long/url"
    }
    ```
  - Unique Index: `short_code` (unique constraint for collision prevention)
- Persistence: Data persisted in MongoDB; survives application restarts.
- Default Database: `url_shortener`

Short-code Generation
- Approach: 6-character alphanumeric code.
- Alphabet: `0-9`, `a-z`, `A-Z` (62 characters).
- Algorithm: Generate random code, check for collisions in dictionary, retry if collision found.
- Collision handling: Re-generate if code already exists (extremely rare).

URL Validation
- Validate: absolute URL with `http://` or `https://` protocol.
- Check: URL length ≤ 2048 characters.
- Library: `urllib.parse` for parsing.

Scenarios
- Happy path: `POST /shorten` with valid URL → generate code → return 201.
- Redirect: `GET /abc123` → redirect to original URL with 301.
- Invalid URL: `POST /shorten` with malformed URL → return 400.
- Unknown code: `GET /invalid` → return 404.

Error Codes
- 201 Created
- 301 Permanent Redirect
- 400 Bad Request
- 404 Not Found
- 500 Server Error

Implementation Notes (Python)
- Framework: **FastAPI** (lightweight, simple routing)
- Database: **MongoDB** with PyMongo driver
- HTTP Client: `requests` for testing
- URL Parsing: `urllib.parse`
- Testing: `pytest`
- Storage: MongoDB document-based persistence
- Connection: Configurable via `MONGODB_URI` environment variable (default: `mongodb://127.0.0.1:27017/`)

— End of Basic URL Shortener SRS —