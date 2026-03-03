def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"