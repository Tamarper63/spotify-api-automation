# Spotify API Automation

## Overview
End-to-end automation test suite for the **Spotify Web API**, built for:
- **Full endpoint coverage**: playlists, search, browse, user profile/history.
- **Unified transport layer**: all HTTP requests routed via `RequestHandler.send()` with retries, backoff, and logging.
- **Config-driven architecture**: Pydantic-based `AppConfig` with `.env` support.
- **NLP → API (LLM Integration)**: Translate natural language into valid Spotify API requests using a local LLM (Ollama).
- **Maintainable test design**: modular, SRP-aligned, ready for CI/CD.

---

## 🚀 Quickstart

```bash
# Clone repository
git clone https://github.com/YOUR_ORG/spotify-api-automation.git
cd spotify-api-automation

# Install dependencies
pip install -r requirements.txt

# Copy example env file and edit values
cp .env.example .env

# Run all tests
pytest --disable-warnings -v

# Generate HTML test report
pytest --html=reports/report.html
```

---

## 🧠 LLM Feature: NLP → API
This feature converts **natural language queries** into structured Spotify Web API requests.

**Example:**
```bash
python scripts/run_nlp_query.py
```
**Input:**
```
תראה לי את האומנים הכי מושמעים שלי
```
**Output:**
```
--- NLP → API Result ---
Method: GET
URL: https://api.spotify.com/v1/me/top/artists
Headers: {...}
Body: None
```

**Configuration:**
- `.env` must include:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral
```
- Requires [Ollama](https://ollama.com/) running locally (`brew install ollama`).

---

## 🏗 Project Structure

```
project/
├── infra/
│   ├── api_clients/         # SpotifyClient - thin endpoint wrappers
│   ├── auth/                # TokenManager & providers
│   ├── config/              # AppConfig (pydantic settings)
│   ├── http/                # RequestHandler + _send_request
│   └── models/              # Pydantic schemas
├── tests/
│   ├── playlists/           # Unified per-endpoint test suites
│   ├── browse/              # Featured playlists
│   ├── search/              # Search endpoint
│   ├── user/                # User profile/history
│   └── data/assets/         # Test images, payloads
├── utils/                   # Logging, assertions, image utils
├── scripts/                 # CLI scripts (incl. NLP → API runner)
├── reports/                 # HTML & coverage reports
├── requirements.txt
└── README.md
```

---

## 🔐 Authentication

**Supported flows:**
- **Client Credentials Flow** (App token)
- **Authorization Code Flow** (User token)

**Env variables:**
```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
SPOTIFY_REFRESH_TOKEN=...
SPOTIFY_USER_ACCESS_TOKEN=...
DEFAULT_PLAYLIST_ID=...
```

---

## 🧪 Test Strategy
- **Framework**: pytest
- **Fixtures**: centralized in `conftest.py`
- **Structure**: endpoint-focused test files (positive + negative in same file)
- **Tags**: `@pytest.mark.positive` / `@pytest.mark.negative`
- **Flow tests**: E2E scenario in `test_playlist_flow.py`

Example:
```python
@pytest.mark.positive
def test_create_playlist_should_return_201(spotify_user_client, user_id):
    response = spotify_user_client.create_playlist(user_id, "Automation Playlist")
    assert response.status_code == 201
```

---

## ⚙️ Configuration
- **File**: `infra/config/settings.py`
- **Base**: Pydantic `BaseSettings`
- **Extra handling**: `extra="ignore"` to allow unrelated env vars (e.g., `LLM_PROVIDER`).

---

## 📊 Reports
Generate HTML report:
```bash
pytest --html=reports/report.html
```
Coverage report:
```bash
pytest --cov=.
```

---

## 🧼 Code Quality
- **No dead code** (validated)
- **Centralized HTTP transport**
- **Logging**: unified via `log_api_call`
- **SOLID** principles applied in client/auth/http layers

---

## 🛠 CI/CD Ready
- Easily integrated with GitHub Actions, CircleCI, or Jenkins
- Output includes test results, coverage, and logs

---

## 🧩 Contributing
1. Fork the repo
2. Create a branch (`feature/xyz`)
3. Run `black`, `flake8`, and `pytest`
4. Open PR with context and references

---

## 📚 References
- [Spotify API Docs](https://developer.spotify.com/documentation/web-api)
- [Pytest Docs](https://docs.pytest.org)
- [Pydantic](https://docs.pydantic.dev)
- [Ollama](https://ollama.com/)

---

## 📄 License
MIT © [YOUR_ORG]
