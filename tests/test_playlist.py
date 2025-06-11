def test_create_playlist_returns_201(api_clients, report):
    # Arrange
    playlist_client = api_clients.playlist
    user_client = api_clients.user

    user_id = user_client.get_me().json()["id"]

    # Act
    response = playlist_client.create_playlist(user_id, name="Smoke Playlist")

    # Assert
    assert response.status_code == 201, "Expected 201 Created"
    data = response.json()
    assert data["name"] == "Smoke Playlist"
    assert data["public"] is True
    assert "id" in data
