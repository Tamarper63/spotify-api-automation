import webbrowser
import urllib.parse

from infra.auth.user_token_provider import exchange_code_for_token, refresh_token


class OAuthHandler:
    AUTH_URL = "https://accounts.spotify.com/authorize"

    def __init__(self, client_id, client_secret, redirect_uri, scopes):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes

    def get_authorization_url(self) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "show_dialog": "true",
        }
        return f"{self.AUTH_URL}?{urllib.parse.urlencode(params)}"

    def authorize(self) -> dict:
        """
        Interactive authorization flow: opens browser and waits for user to paste code.
        """
        url = self.get_authorization_url()
        webbrowser.open(url)
        auth_code = input("🔐 Paste the redirected code here: ").strip()
        return self.exchange_code_for_token(auth_code)

    def exchange_code_for_token(self, code: str) -> dict:
        return exchange_code_for_token(
            code=code,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )

    def refresh_user_token(self, token: str) -> dict:
        return refresh_token(token, self.client_id, self.client_secret)
