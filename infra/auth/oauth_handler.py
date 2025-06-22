import requests
import webbrowser
import urllib.parse
import base64


class OAuthHandler:
    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, redirect_uri, scopes):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes

    def authorize(self):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "show_dialog": "true",  # ✅ Force Spotify to show the consent screen
        }

        url = f"{self.AUTH_URL}?{urllib.parse.urlencode(params)}"
        webbrowser.open(url)
        auth_code = input("🔐 Paste the redirected code here: ").strip()

        return self.exchange_code_for_token(auth_code)

    def exchange_code_for_token(self, code):
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,  # ✅ Add this
            "client_secret": self.client_secret  # ✅ And this
        }

        response = requests.post(self.TOKEN_URL, headers=headers, data=data)

        # ✅ Print error if it fails
        if not response.ok:
            print(f"[ERROR] {response.status_code}: {response.text}")

        response.raise_for_status()
        return response.json()

    def refresh_user_token(self, refresh_token: str) -> dict:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            auth=(self.client_id, self.client_secret),
        )
        response.raise_for_status()
        return response.json()
