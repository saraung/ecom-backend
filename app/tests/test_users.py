from app.tests.conftest import _register_and_login, _make_superuser


def test_create_user_as_admin(client, admin_headers):
    """Superuser can create a user."""
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"},
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_create_user_unauthorized(client):
    """Anonymous user gets 401."""
    resp = client.post(
        "/users/",
        json={"email": "anon@example.com", "password": "password123"},
    )
    assert resp.status_code == 401


def test_create_user_forbidden(client, auth_headers):
    """Regular user gets 403 on admin route."""
    resp = client.post(
        "/users/",
        json={"email": "forbidden@example.com", "password": "password123"},
        headers=auth_headers,
    )
    assert resp.status_code == 403


def test_get_own_user(client, db):
    """User can view their own profile."""
    headers = _register_and_login(client, "self@example.com")
    # get own user id via /auth/me
    me = client.get("/auth/me", headers=headers).json()
    resp = client.get(f"/users/{me['id']}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "self@example.com"


def test_get_other_user_forbidden(client, db):
    """Regular user cannot view other users."""
    headers_a = _register_and_login(client, "usera@example.com")
    headers_b = _register_and_login(client, "userb@example.com")
    me_b = client.get("/auth/me", headers=headers_b).json()
    resp = client.get(f"/users/{me_b['id']}", headers=headers_a)
    assert resp.status_code == 403


def test_get_user_not_found(client, admin_headers):
    resp = client.get("/users/9999", headers=admin_headers)
    assert resp.status_code == 404


def test_update_own_user(client, db):
    """User can update their own profile."""
    headers = _register_and_login(client, "update@example.com")
    me = client.get("/auth/me", headers=headers).json()
    resp = client.put(
        f"/users/{me['id']}",
        json={"email": "updated@example.com"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["email"] == "updated@example.com"


def test_update_user_privilege_escalation_blocked(client, db):
    """Regular user cannot set is_superuser or is_active."""
    headers = _register_and_login(client, "escalate@example.com")
    me = client.get("/auth/me", headers=headers).json()
    resp = client.put(
        f"/users/{me['id']}",
        json={"is_superuser": True},
        headers=headers,
    )
    assert resp.status_code == 403


def test_delete_user_as_admin(client, admin_headers):
    """Superuser can delete a user."""
    create_resp = client.post(
        "/users/",
        json={"email": "delete@example.com", "password": "password123"},
        headers=admin_headers,
    )
    user_id = create_resp.json()["id"]
    resp = client.delete(f"/users/{user_id}", headers=admin_headers)
    assert resp.status_code == 204
    resp = client.get(f"/users/{user_id}", headers=admin_headers)
    assert resp.status_code == 404


def test_delete_user_forbidden(client, auth_headers):
    """Regular user cannot delete users."""
    resp = client.delete("/users/1", headers=auth_headers)
    assert resp.status_code == 403


def test_list_users_as_admin(client, admin_headers):
    """Superuser can list all users."""
    resp = client.get("/users/", headers=admin_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_list_users_forbidden(client, auth_headers):
    """Regular user cannot list all users."""
    resp = client.get("/users/", headers=auth_headers)
    assert resp.status_code == 403