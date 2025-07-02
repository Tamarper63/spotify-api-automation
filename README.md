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
├── auth/
│ └── token_manager.py # Token flows
├── config/
│ └── settings.py # .env + secrets
├── http/
│ ├── request_sender.py # Low-level HTTP
│ └── request_handler.py # Injected wrapper with logging & metrics
├── models/ # Pydantic models
tests/
├── playlists/
├── search/
├── user/
├── browse/
├── auth/
└── conftest.py # Fixtures & test setup
utils/
├── assertion_manager.py # Assertions & response validation
├── image_utils.py # Image helper utilities
└── yaml_loader.py # YAML parametric test data loader

yaml
Copy

---

## 🧪 Test Capabilities

- ✅ Positive, contract, smoke tests  
- ❌ Negative cases: unauthorized, invalid params validations  
- ✅ End-to-end lifecycle validation (`test_playlist_flow.py`)  
- ✅ YAML-based parametric testing (pagination, limit-offset)  
- ✅ Model schema assertions with `assert_response_schema(...)`  

---

## 🔐 Auth Token Flow

```python
from infra.auth.token_manager import TokenManager

# Get app-level client token
client_token = TokenManager.get_token()

# Get user-level OAuth token (auto refresh)
user_token = TokenManager.get_user_token()

# All API calls routed via RequestHandler(token)
🚀 Run Tests Locally
bash
Copy
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
Run filtered tests by marker:
pytest -m "positive"
pytest -m "contract"

Generate HTML report:
pytest --html=reports/html/report.html --self-contained-html

🐳 Run Tests with Docker Compose
Prerequisites: Docker installed and running.

Create .env file in project root with all required environment variables (see below).

Run tests in isolated container with dependencies and environment:

bash
Copy
docker-compose up --build
This builds the Docker image and runs all tests inside a consistent, isolated environment.

⚙ Environment Variables (.env)
Required variables:

env
Copy
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_USER_ACCESS_TOKEN=your_user_access_token
SPOTIFY_REFRESH_TOKEN=your_refresh_token
SPOTIFY_USER_EXPIRES_AT=expiry_timestamp
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
DEFAULT_PLAYLIST_ID=your_default_playlist_id
🧭 Usage Example (Python Client)
python
Copy
from infra.api_clients.spotify_client import SpotifyClient
from infra.http.request_handler import RequestHandler

request_handler = RequestHandler(user_token)  # Use user token or client token as needed
client = SpotifyClient(request_handler)

# Playlist operations
playlist = client.get_playlist("playlist_id")
client.add_tracks_to_playlist("playlist_id", ["spotify:track:..."])

# Search operations
results = client.search(query="Nirvana", types=["track"])

# User profile
profile = client.get_current_user_profile()
Notes
Use pytest markers for targeted test runs.

The automation framework includes logging, API request timing, and response schema validation for reliability.

Docker integration ensures repeatable test environments and dependency isolation.


