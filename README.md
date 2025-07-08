# Spotify API Automation

[![Test Suite](https://img.shields.io/badge/tests-passing-brightgreen)](./reports)  
[![Coverage](https://img.shields.io/badge/coverage-95%25-green)](./reports)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

> **End-to-end automation suite for the Spotify Web API**
> - Full test coverage over major playlist/user/search endpoints
> - Refactored client design with unified handlers, token flow, and log layer
> - Built for modularity, maintainability, and fast regression tracking

---

## 🚀 Quickstart

```bash
git clone https://github.com/YOUR_ORG/spotify-api-automation.git
cd spotify-api-automation

# Install dependencies (in a virtualenv)
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Insert your Spotify credentials in .env

# Run tests
pytest --maxfail=1 --disable-warnings -v

# Generate HTML report
pytest --html=reports/report.html
```

---

## 🏗️ Project Structure

```
project/
├── infra/
│   ├── api_clients/         # SpotifyClient: All endpoint wrappers
│   ├── auth/                # TokenManager: user/client flows
│   ├── config/              # .env parser + config loader
│   ├── http/                # Unified request sender + response handler
│   └── models/              # Pydantic schemas (used & optimized only)
├── tests/
│   ├── playlists/           # Unified + refactored tests per endpoint
│   ├── browse/              # Featured playlists
│   ├── search/              # /search endpoint tests
│   ├── user/                # Top artists, profile, history
│   └── data/assets/         # JPEGs, base64, static data
├── utils/                   # image_utils, assertions, logging
├── scripts/                 # CLI runners and test entrypoints
├── reports/                 # Test results & coverage HTML
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

- **Architecture**: Layered + isolated per concern  
- **Clients**: Single entrypoint via `SpotifyClient`  
- **HTTP**: Central `_send_request()` with logging/metrics  
- **Auth**: `TokenManager` with support for both flows  
- **Tests**: Fully migrated, each endpoint has one refactored suite  

---

## 🔐 Authentication

- Supports:
  - **Client Credentials Flow**  
  - **Authorization Code Flow (User Token)**  
- Tokens managed via `infra/auth/token_manager.py`  
- Test isolation per token type  
- `.env` defines all secrets

---

## 🧪 Test Strategy

- **Framework**: `pytest`  
- **Structure**: Flat test files per endpoint, both positive and negative  
- **Fixtures**: Shared via `conftest.py`  
- **Data**: JPEGs, invalid payloads, base64 files – in `/tests/data/assets/`  
- **Tags**: `@pytest.mark.positive`, `@pytest.mark.negative`  
- **Flow Test**: End-to-end created under `test_playlist_flow.py`

#### Example:
```python
@pytest.mark.positive
def test_update_playlist_cover_image_valid():
    image_data = load_valid_base64_image("test.jpg")
    response = spotify_user_client.update_playlist_cover_image(playlist_id, image_data)
    assert response.status_code == 202
```

---

## ⚙️ Configuration

- All configuration handled via `infra/config/settings.py`  
- `.env` file defines:
  - Client ID / Secret  
  - Redirect URI  
  - Test playlist ID, etc.

---

## 📊 Reports

- HTML test reports generated via `pytest-html`  
- Located in `./reports/report.html`  
- Coverage reports available via `pytest-cov`

---

## 🧼 Code Quality

- No unused imports, duplications, or dead code (validated)  
- `log_utils.py` wraps all API calls with timing, response tracking  
- SOLID & SRP enforced across models and utilities  
- All code reviewed and normalized across modules  

---

## 🛠 CI/CD Ready

- Can be integrated into GitHub Actions, CircleCI or local pipelines  
- Output includes test status, coverage, and refactor logs

---

## 🧩 Contributing

1. Fork repo  
2. Create branch (`feature/xyz`)  
3. Run formatters + tests (`black`, `flake8`, `pytest`)  
4. Open PR with context and references

---

## 📚 References

- [Spotify API Docs](https://developer.spotify.com/documentation/web-api)  
- [Pytest Docs](https://docs.pytest.org/)  
- [Pydantic](https://docs.pydantic.dev/)  
- [pytest-html](https://pypi.org/project/pytest-html/)

---

## 📄 License

MIT © [YOUR_ORG]

---

*For architecture questions, bug reports, or feature requests, please open a GitHub issue.*
