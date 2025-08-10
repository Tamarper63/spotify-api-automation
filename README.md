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
 Which endpoint allows me to update playlist details?
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


## AI-Assisted Documentation Chat (`run_doc_chat`)

This project includes an AI-assisted Documentation Chat tool integrated into the automation framework. 
The `run_doc_chat` script allows developers and QA engineers to query project documentation through a Retrieval-Augmented Generation (RAG) pipeline and receive precise, context-based answers from a local LLM (Ollama).

### Features
- **Local LLM (Ollama) Integration**: Runs fully offline without cloud dependencies.
- **RAG Context Retrieval**: Retrieves the most relevant documentation snippets from local sources before answering.
- **Context-Constrained Responses**: AI responds only with information present in the retrieved context.
- **Developer-Friendly Output**: Technical, concise, and ready for integration into development/test workflows.

### Prerequisites
- **Python**: 3.9+
- **Ollama**: Installed locally and running (default: `http://localhost:11434`)
- **Model**: A supported model pulled locally, for example:
  ```bash
  ollama pull llama3
  ```
- **Dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

### Environment Variables
```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3
OLLAMA_HOST=http://localhost:11434
```
> The RAG retriever expects your documentation to be indexed and accessible to `tools.rag.search.retrieve`.

### Usage
Interactive mode:
```bash
python run_doc_chat.py
```
Example:
```
>> Doc Chat (Ollama). Press Ctrl+C to exit.

Question: How do I authenticate with the Spotify API?
Answer:
[Technical explanation sourced only from context...]
```

Optional arguments:
```bash
python run_doc_chat.py -k 8 --temperature 0.0 --stream
```
- `-k`: Number of context chunks to retrieve (default: 6).
- `--temperature`: LLM sampling temperature (default: 0.1).
- `--stream`: Enable streaming responses (if supported).

### Best Practices
- Keep documentation updated so the retriever returns accurate results.
- Use specific, technical questions for more precise answers.
- Regularly verify Ollama model and retriever configurations.

### Relevant Project Structure
```
project_root/
│
├── tools/
│   ├── rag/
│   │   └── search.py               # Context retrieval logic
│   └── local_llm/
│       └── ollama_client.py        # Ollama API client
│
├── run_doc_chat.py                  # Entry point script
└── docs/                            # Documentation corpus used by RAG
```
