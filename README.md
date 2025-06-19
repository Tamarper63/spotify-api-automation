# 🎧 Spotify API Automation Framework

A robust and scalable **API automation framework** for the [Spotify Web API](https://developer.spotify.com/documentation/web-api/), built in **Python** with **Pytest**, following modern best practices: **SOLID principles**, strict typing, modular design, and schema validation using **Pydantic**.

---

## 📁 Project Structure

spotify-api-automation/
│
├── infra/
│ ├── auth/ # Token manager, authentication handling
│ ├── api_clients/ # Client classes for Spotify endpoints
│ └── models/ # Pydantic schema models for API responses
│
├── tests/
│ ├── auth/ # Token-related tests
│ ├── playlists/ # Playlist endpoint tests
│ └── data/ # YAML parameterized test data
│
├── utils/
│ ├── assertion_manager.py # Centralized reusable assertions
│ ├── schema_validator.py # Schema validation logic
│
├── conftest.py # Centralized fixtures (clients, tokens, configs)
├── requirements.txt
├── pytest.ini
└── README.md

yaml
Copy
Edit

---

## ✅ Example: Token API Tests

### `tests/auth/test_token.py`

Test coverage includes:

| Test Type        | Description                                                |
|------------------|------------------------------------------------------------|
| ✅ Positive       | Validate token creation with valid credentials             |
| ❌ Negative       | Invalid/missing credentials, headers, malformed grant types |
| 🧪 Schema         | Full response validation against strict `TokenResponse` model |

```python
@pytest.mark.positive
def test_token_success_with_valid_credentials():
    client = AuthClient()
    full_response = client.get_token_response()

    assert_response_schema(full_response, TokenResponse, context="Smoke test: Get token")
    assert_token_is_valid(full_response["access_token"])
🧠 Framework Features
✅ Pytest with tags: @positive, @negative, @smoke, etc.

✅ Pydantic for strict schema models

✅ Environment-safe using python-dotenv

✅ SOLID test design: no logic inside test bodies

✅ Reusable validation via AssertionManager

✅ YAML-ready for future data-driven test expansion


🔐 Environment Variables
Add a .env file in the root:

dotenv
Copy
Edit
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
These are accessed by ConfigManager via load_dotenv().

🚀 How to Run
1. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
2. Run all tests
bash
Copy
Edit
pytest -v
3. Generate HTML report
bash
Copy
Edit
pytest --html=report.html --self-contained-html
📦 Models Example
infra/models/token_response.py

python
Copy
Edit
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
👨‍🔬 Assertions Example
utils/assertion_manager.py

python
Copy
Edit
def assert_token_is_valid(token: str):
    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 20, "Token seems unexpectedly short"
🧪 Test Tags & Strategy
@pytest.mark.positive: expected successful flow

@pytest.mark.negative: validation and failure handling

@pytest.mark.contract: response structure and type checks

@pytest.mark.smoke: essential flows to validate availability

👩‍💻 Author
Tamar Peretz
Senior Infrastructure & API Automation Engineer
Maintaining this repo as a real-world example of best practices for API test architecture.

