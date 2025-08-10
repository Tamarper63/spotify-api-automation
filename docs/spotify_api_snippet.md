# Spotify Web API – Covered Endpoints (Automation Project)

---

## 1. PUT /v1/playlists/{playlist_id}/followers

### Description
Follow or unfollow a playlist.

### Path Parameters
- `playlist_id` (required): The Spotify ID of the playlist

### Request Body
```json
{
  "public": true
}
```

### Headers
- Authorization: Bearer token

---

## 2. GET /v1/browse/featured-playlists

### Description
Returns a list of Spotify featured playlists.

### Query Parameters
- `country` (optional): ISO 3166-1 alpha-2 country code (e.g., "IL", "US")
- `locale` (optional): Language and country code (e.g., "en_US")
- `timestamp` (optional): ISO 8601 timestamp
- `limit` (optional): Default 20, Max 50
- `offset` (optional): Index of first item

---

## 3. GET /v1/search

### Description
Search for albums, artists, playlists, tracks, shows, episodes, or audiobooks.

### Query Parameters
- `q` (required): Search query keywords
- `type` (required): Comma-separated list of item types to search across
- `market` (optional): ISO 3166-1 alpha-2 country code
- `limit` (optional): Default 20, Max 50
- `offset` (optional): Index of first result

---

## 4. GET /v1/me/top/artists

### Description
Get the current user’s top artists based on calculated affinity.

### Query Parameters
- `time_range` (optional): short_term, medium_term, long_term
- `limit` (optional): Default 20, Max 50
- `offset` (optional): Index of first item

---

## 5. GET /v1/me/player/recently-played

### Description
Get tracks from the current user’s recently played items.

### Query Parameters
- `limit` (optional): Default 20, Max 50
- `after` / `before` (optional): UNIX timestamp (ms)

---

## 6. POST /v1/users/{user_id}/playlists

### Description
Create a playlist for a Spotify user.

### Path Parameters
- `user_id` (required): The user ID

### Request Body
```json
{
  "name": "My Playlist",
  "description": "Some description",
  "public": false
}
```

---

## 7. GET /v1/playlists/{playlist_id}

### Description
Get a playlist owned by a Spotify user.

### Path Parameters
- `playlist_id` (required): The Spotify ID of the playlist

### Query Parameters
- `market` (optional): ISO 3166-1 alpha-2 country code
- `fields` (optional): Filters for the query

---

## 8. GET /v1/playlists/{playlist_id}/tracks

### Description
Get full details of the tracks of a playlist.

### Path Parameters
- `playlist_id` (required): The Spotify ID of the playlist

### Query Parameters
- `market` (optional)
- `fields` (optional)
- `limit` (optional): Default 100, Max 100
- `offset` (optional): Index of first track

---

## 9. POST /v1/playlists/{playlist_id}/tracks

### Description
Add one or more items to a user's playlist.

### Path Parameters
- `playlist_id` (required): The Spotify ID of the playlist

### Request Body
```json
{
  "uris": ["spotify:track:abc", "spotify:track:def"],
  "position": 0
}
```

---

## 10. DELETE /v1/playlists/{playlist_id}/tracks

### Description
Remove one or more items from a user's playlist.

### Path Parameters
- `playlist_id` (required): The Spotify ID of the playlist

### Request Body
```json
{
  "tracks": [
    { "uri": "spotify:track:abc" },
    { "uri": "spotify:track:def" }
  ]
}
```

---

## 11. PUT /v1/playlists/{playlist_id}

### Description
Change a playlist’s name and public/private state.

### Path Parameters
- `playlist_id` (required): The Spotify ID of the playlist

### Request Body
```json
{
  "name": "New name",
  "public": false,
  "description": "Updated description"
}
```

---

## 12. PUT /v1/playlists/{playlist_id}/images

### Description
Replace the image used to represent a playlist.

### Path Parameters
- `playlist_id` (required): The Spotify ID of the playlist

### Headers
- Content-Type: image/jpeg
- Authorization: Bearer token

### Body
Base64 encoded JPEG image (max size: 256 KB)