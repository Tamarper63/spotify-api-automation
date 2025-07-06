# scripts/create_playlist.py

import requests
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN = os.getenv("SPOTIFY_USER_ACCESS_TOKEN")
BASE_URL = "https://api.spotify.com/v1"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

# Step 1: Get current user's ID
user_response = requests.get(f"{BASE_URL}/me", headers=headers)
user_response.raise_for_status()
user_id = user_response.json()["id"]

# Step 2: Create a new playlist
data = {
    "name": "Automation Test Playlist",
    "description": "Playlist created via API test",
    "public": False,
}

create_response = requests.post(
    f"{BASE_URL}/users/{user_id}/playlists", headers=headers, json=data
)
create_response.raise_for_status()

playlist_id = create_response.json()["id"]
playlist_url = create_response.json()["external_urls"]["spotify"]

print(f"✅ Playlist created: {playlist_url}")
print(f"🆔 Playlist ID: {playlist_id}")
