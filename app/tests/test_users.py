def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_user(client):
    # create
    create_resp = client.post(
        "/users/",
        json={"email": "get@example.com", "password": "password123"},
    )
    user_id = create_resp.json()["id"]

    # fetch
    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    assert resp.json()["email"] == "get@example.com"


def test_get_user_not_found(client):
    resp = client.get("/users/9999")
    assert resp.status_code == 404


def test_update_user(client):
    create_resp = client.post(
        "/users/",
        json={"email": "update@example.com", "password": "password123"},
    )
    user_id = create_resp.json()["id"]

    resp = client.put(
        f"/users/{user_id}",
        json={"email": "updated@example.com"},
    )
    assert resp.status_code == 200
    assert resp.json()["email"] == "updated@example.com"


def test_delete_user(client):
    create_resp = client.post(
        "/users/",
        json={"email": "delete@example.com", "password": "password123"},
    )
    user_id = create_resp.json()["id"]

    resp = client.delete(f"/users/{user_id}")
    assert resp.status_code == 204

    # verify gone
    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 404


def test_list_users(client):
    client.post("/users/", json={"email": "list@example.com", "password": "pass"})
    resp = client.get("/users/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)