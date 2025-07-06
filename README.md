
# Spotify API Automation

[![Test Suite](https://img.shields.io/badge/tests-passing-brightgreen)](./reports)
[![Coverage](https://img.shields.io/badge/coverage-95%25-green)](./reports)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

> **End-to-end automation and validation suite for the Spotify Web API**
> - Unified client architecture, layered config, and strict modular conventions
> - Designed for reliability, coverage, and maintainability at scale

---

## 🚀 Quickstart

```bash
git clone https://github.com/YOUR_ORG/spotify-api-automation.git
cd spotify-api-automation

# Install dependencies (preferably in a venv)
pip install -r requirements.txt

# Set up environment (copy .env.example to .env and fill secrets)
cp .env.example .env
# Edit .env with your Spotify API credentials

# Run full test suite
pytest --maxfail=1 --disable-warnings -v

# Generate HTML report (optional)
pytest --html=reports/report.html
```

---

## 🏗️ Architecture Overview

```
project/
├── infra/
│   ├── api_clients/      # SpotifyClient (all endpoints)
│   ├── auth/             # Token flows (user, client)
│   ├── config/           # Settings, .env, config manager
│   ├── http/             # Low-level HTTP & handlers
│   └── models/           # Pydantic response schemas
├── tests/
│   ├── playlists/        # Playlist endpoint tests
│   ├── search/           # Search API tests
│   ├── user/             # User profile/tests
│   ├── browse/           # Browse/featured API tests
│   └── conftest.py       # Pytest fixtures
├── utils/                # Assertions, images, logging
├── scripts/              # CLI/test runners, helpers
├── reports/              # Test and coverage reports
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container support
├── docker-compose.yml    # Local infra orchestration
└── README.md
```

- **Pattern**: Layered (Infra, Client, Models, Tests, Utils)
- **Token Handling**: Centralized via `TokenManager`
- **All HTTP**: Routed via `RequestHandler` for logging/metrics
- **Schema**: Strict Pydantic models

---

## 🔐 Authentication

- Supports both Client Credentials and User Auth (Authorization Code Flow)
- Secrets managed via `.env` and `infra/config/settings.py`
- Safe token propagation for all tests

---

## 🧪 Test Structure

- **Framework**: [pytest](https://docs.pytest.org/)
- **Discovery**: All tests under `/tests`, modularized per API
- **Fixtures**: Isolated and reusable, found in `conftest.py`
- **Tags/Markers**: `@pytest.mark.positive`, `@pytest.mark.negative`
- **Data**: Static data in `/tests/data`, YAML or JSON
- **Coverage**: Reports in `/reports` (HTML via pytest-html)

#### Example

```python
@pytest.mark.positive
def test_create_playlist(spotify_user_client, user_id):
    playlist = spotify_user_client.create_playlist(user_id, name="My Playlist")
    assert playlist["name"] == "My Playlist"
```

---

## ⚙️ Configuration

- All config is handled via `.env` and `infra/config/settings.py`
- Supports secret rotation, custom endpoints, and local/CI overrides

---

## 🏆 Best Practices

- No unused imports, dead code, or test debris (checked by CI)
- Unified logging via `log_utils` for all HTTP and API calls
- SRP: Each model, service, and utility with single, testable responsibility
- Validated against high-standard public repos

---

## 🤝 Contributing

1. Fork this repo
2. Create a branch (`feature/xyz`)
3. Run lint (`flake8`), format (`black`), and full tests (`pytest`)
4. Open a PR—describe context and changes

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## 📄 Documentation

- [Spotify API Docs](https://developer.spotify.com/documentation/web-api)
- [Pytest Docs](https://docs.pytest.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

## 🛡️ License

MIT License (c) [YOUR_ORG]

---

*For architecture questions, bug reports, or feature requests, please open a GitHub issue.*
