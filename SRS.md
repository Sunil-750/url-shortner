**Short URL Service — SRS (condensed)**

Project: URL Shortener
Location: `/Users/sunilsahu/Desktop/Code/Paytm/url-shortner`
Objective: Convert long URLs to short, URL-safe codes and redirect visitors to originals.

Purpose
- Provide a concise, implementable specification covering API, storage, validation, short-code generation, custom aliases, duplicate handling, and operational concerns.

Scope
- In-scope: `POST /shorten`, `GET /{code}`, persistent mappings, custom aliases, 301 redirects, URL validation, deterministic duplicate handling.
- Out-of-scope: authentication, analytics UI, bulk import/export, advanced spam detection.

Key Definitions
- Short code: short URL-safe identifier (e.g., `b9Xy2A`).
- Custom alias: user-specified `code` (e.g., `sale-2026`).
- Base62: `0-9A-Za-z` character set.

Functional Requirements (summary)
- POST /shorten
  - Request JSON: `{ "url": "<absolute-url>", "alias": "optional", "force_new": false }`.
  - Validate URL (http/https), alias charset (`[A-Za-z0-9-_]`) and length (3–100), max URL length 2048.
  - If `alias` provided: try atomic insert; on success return 201 with the alias; on unique violation return 409.
  - If no alias: canonicalize URL, if existing mapping found return that code (idempotent), else create new mapping and return 201 with generated code. `force_new=true` overrides idempotency.
- GET /{code}
  - If mapping exists return `301` with `Location: <original_url>`; else `404` with `{ "error": "code_not_found" }`.

Duplicate URL Policy
- Default: idempotent — same canonical URL returns existing code. Optionally `force_new` to create another.

Data Model
- Datastore: PostgreSQL (primary) + Redis (optional cache).
- Table `urls` (suggested):
  - `id` bigserial PK
  - `code` text UNIQUE NOT NULL
  - `original_url` text NOT NULL
  - `created_at` timestamptz DEFAULT now()
  - `owner` nullable
  - `clicks` bigint DEFAULT 0
  - Indexes: unique on `code`; index on `original_url` for duplicate lookup.

Short-code Generator
- Approach: DB sequence id → Base62 encoding.
  - Flow: INSERT (RETURNING id) → encode id to Base62 → update `code` (or compute from sequence before insert).
  - Rationale: deterministic, simple, collision-free because DB sequence guarantees unique ids; Base62 yields URL-safe compact codes.
  - Capacity: 6 chars ≈ 62^6 ≈ 57B codes; variable length is fine.
  - Concurrency: DB sequence and unique constraint prevent collisions under concurrent writes.
- Alternate: UUID/hash (longer, collision risk if truncated).

URL Validation & Canonicalization
- Validate: absolute URL with `http`/`https`; reject `file:`, `data:`, `javascript:`; enforce max length.
- Canonicalize before duplicate-detection: lowercase host, remove default ports, trim whitespace. Sorting query params is optional (configurable) because it can change semantics.

Scenarios (condensed)
- Happy path: POST a valid URL → insert → id→Base62 `dnh` → GET `/dnh` → 301 to original.
- Custom alias success: POST with alias `sale-2026` → atomic insert → 201 → GET `/sale-2026` → 301.
- Alias conflict: POST with taken alias → 409 `{ "error":"alias_taken" }`.
- Duplicate shorten: repost same canonical URL → return existing code (no new record) unless `force_new`.
- Invalid URL: return 400 `{ "error":"invalid_url" }`.
- Unknown code: GET unknown → 404.
- Concurrency: DB sequence ensures uniqueness.

Error Codes
- 201 Created, 200 OK (optional for existing mapping), 301 Redirect, 400 Bad Request, 404 Not Found, 409 Conflict, 429 Rate-limited, 500 Server error.

Security & Operational Notes
- TLS required; rate-limit `POST /shorten` (per-IP, per-key); input sanitization; log safely (avoid PII).
- Monitor creation rate, errors, redirect latency; backup Postgres and test restores.
- Mitigate open-redirect abuse with heuristics/whitelists if required.

Scalability
- Cache code→URL in Redis to serve redirects quickly; scale app instances horizontally; rely on DB for unique id generation or move to sharded ID generator for extreme scale.

Risks & Trade-offs
- Sequential ids leak volume (mitigate with salted/offset mapping). Canonicalization may change semantics. Custom aliases can be abused — require moderation.

Implementation Notes & Next Steps
- Use robust URL parsing library (e.g., `urllib.parse` or `java.net.URI`).
- Implement minimal server with `POST /shorten` and `GET /{code}`, DB migration SQL, tests for scenarios, Redis caching, and rate-limiting.

Appendix — Base62 (sketch)
- alphabet: `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`.
- encode: repeatedly divide id by 62 and map remainders.
- example flow: `id = INSERT ... RETURNING id; code = base62(id); UPDATE urls SET code=...`.

— End of condensed SRS —