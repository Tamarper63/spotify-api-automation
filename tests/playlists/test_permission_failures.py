
def test_action_requiring_permission_should_fail_without_scope(spotify_user_client):
    response = spotify_user_client.create_playlist(user_id="some_id", name="test")
    assert response.status_code in (401, 403)
