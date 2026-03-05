def test_register(client):
    resp = client.post(
        "/auth/register",
        json={"email": "newuser@test.com", "password": "secret123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "newuser@test.com"
    assert "id" in data


def test_register_duplicate(client):
    client.post(
        "/auth/register",
        json={"email": "dup@test.com", "password": "secret123"},
    )
    resp = client.post(
        "/auth/register",
        json={"email": "dup@test.com", "password": "secret123"},
    )
    assert resp.status_code == 409


def test_login(client):
    # register first
    client.post(
        "/auth/register",
        json={"email": "login@test.com", "password": "secret123"},
    )
    # login using OAuth2 form
    resp = client.post(
        "/auth/login",
        data={"username": "login@test.com", "password": "secret123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid(client):
    resp = client.post(
        "/auth/login",
        data={"username": "nobody@test.com", "password": "wrong"},
    )
    assert resp.status_code == 401
