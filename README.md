# Spotify API Automation

Automation suite for Spotify Web API with unified client architecture, structured test layers, and strict modular conventions.

---

## ✅ Overview

- 🧱 Architecture: Layered (Config, HTTP, Client, Models, Tests, Utils)
- 🧪 Test Framework: `pytest` with custom markers and assertion manager
- 🔐 Auth Support: Client Credentials + User Token via `TokenManager`
- 🧵 Unified API Client: `SpotifyClient` handles all endpoints (auth, playlist, user, search, browse)
- 📊 Schema validation via `pydantic` models
- 💡 Coverage: Playlists, Tracks, Search, Browse, User Profile

---

## 📂 Project Structure

infra/
├── api_clients/
│ └── spotify_client.py # Unified SpotifyClient
├── auth/token_manager.py # Token flows
├── config/settings.py # .env + secrets
├── http/
│ ├── request_sender.py # Low-level HTTP
│ └── request_handler.py # Injected wrapper
├── models/ # Pydantic models
tests/
├── playlists/
├── search/
├── user/
├── browse/
├── auth/
└── conftest.py # Fixtures
utils/
├── assertion_manager.py
├── image_utils.py
└── yaml_loader.py

yaml
Copy
Edit

---

## 🧪 Test Capabilities

- ✅ Positive / contract / smoke tests
- ❌ Negative / unauthorized / invalid param validations
- ✅ End-to-end lifecycle validation (`test_playlist_flow.py`)
- ✅ YAML-based parametric testing (pagination, limit-offset)
- ✅ Model schema assertion with `assert_response_schema(...)`

---

## 🔐 Auth Token Flow

```python
# Token generation
from infra.auth.token_manager import TokenManager

client_token = TokenManager.get_token()
user_token = TokenManager.get_user_token()
All requests are routed via RequestHandler(token).

🚀 Run Tests
bash
Copy
Edit
# Basic run
pytest

# Filter by marker
pytest -m "positive"
pytest -m "contract"

# Generate HTML report
pytest --html=reports/html/report.html --self-contained-html
🧭 Usage Example
python
Copy
Edit
client = SpotifyClient(request_handler)

# Playlist
client.get_playlist("playlist_id")
client.add_tracks_to_playlist("playlist_id", ["spotify:track:..."])

# Search
client.search(query="Nirvana", types=["track"])

# User
client.get_current_user_profile()
