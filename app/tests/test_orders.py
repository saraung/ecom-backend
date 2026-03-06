from app.tests.conftest import _register_and_login, _make_superuser


def _create_product(client, admin_headers, name="Boots", price=4999.99, stock=5):
    """Helper to create a product as admin."""
    return client.post(
        "/products/",
        json={
            "name": name,
            "description": "Test product",
            "price": price,
            "stock_quantity": stock,
        },
        headers=admin_headers,
    ).json()


def test_create_order_flow(client, db, admin_headers):
    """Authenticated user can create an order (user_id from token)."""
    user_headers = _register_and_login(client, "order@test.com")
    product = _create_product(client, admin_headers)

    response = client.post(
        "/orders/",
        json={
            "items": [{"product_id": product["id"], "quantity": 2}]
        },
        headers=user_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert len(data["items"]) == 1
    assert float(data["total_amount"]) == 4999.99 * 2


def test_create_order_unauthorized(client, admin_headers):
    """Anonymous user gets 401."""
    product = _create_product(client, admin_headers, name="AnonBoot")
    resp = client.post(
        "/orders/",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
    )
    assert resp.status_code == 401


def test_get_own_order(client, db, admin_headers):
    """User can view their own order."""
    user_headers = _register_and_login(client, "getorder@test.com")
    product = _create_product(client, admin_headers, name="Jersey", price=1999.99, stock=10)

    order = client.post(
        "/orders/",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
        headers=user_headers,
    ).json()

    resp = client.get(f"/orders/{order['id']}", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == order["id"]


def test_get_other_user_order_forbidden(client, db, admin_headers):
    """User A cannot view User B's order."""
    headers_a = _register_and_login(client, "owner@test.com")
    headers_b = _register_and_login(client, "intruder@test.com")
    product = _create_product(client, admin_headers, name="Sock", price=99.99, stock=50)

    order = client.post(
        "/orders/",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
        headers=headers_a,
    ).json()

    resp = client.get(f"/orders/{order['id']}", headers=headers_b)
    assert resp.status_code == 403


def test_get_order_not_found(client, auth_headers):
    resp = client.get("/orders/9999", headers=auth_headers)
    assert resp.status_code == 404


def test_get_user_orders_own(client, db, admin_headers):
    """User can list their own orders."""
    user_headers = _register_and_login(client, "myorders@test.com")
    me = client.get("/auth/me", headers=user_headers).json()
    product = _create_product(client, admin_headers, name="Ball", price=149.99, stock=100)

    client.post(
        "/orders/",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
        headers=user_headers,
    )

    resp = client.get(f"/orders/user/{me['id']}", headers=user_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_user_orders_forbidden(client, db, admin_headers):
    """User A cannot list User B's orders."""
    headers_a = _register_and_login(client, "lista@test.com")
    headers_b = _register_and_login(client, "listb@test.com")
    me_b = client.get("/auth/me", headers=headers_b).json()

    resp = client.get(f"/orders/user/{me_b['id']}", headers=headers_a)
    assert resp.status_code == 403


def test_delete_own_order(client, db, admin_headers):
    """User can delete their own order."""
    user_headers = _register_and_login(client, "delorder@test.com")
    product = _create_product(client, admin_headers, name="Socks", price=199.99, stock=50)

    order = client.post(
        "/orders/",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
        headers=user_headers,
    ).json()

    resp = client.delete(f"/orders/{order['id']}", headers=user_headers)
    assert resp.status_code == 204

    resp = client.get(f"/orders/{order['id']}", headers=user_headers)
    assert resp.status_code == 404


def test_delete_other_user_order_forbidden(client, db, admin_headers):
    """User A cannot delete User B's order."""
    headers_a = _register_and_login(client, "delowner@test.com")
    headers_b = _register_and_login(client, "delhacker@test.com")
    product = _create_product(client, admin_headers, name="Cap", price=49.99, stock=30)

    order = client.post(
        "/orders/",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
        headers=headers_a,
    ).json()

    resp = client.delete(f"/orders/{order['id']}", headers=headers_b)
    assert resp.status_code == 403


def test_insufficient_stock(client, db, admin_headers):
    """Order with quantity > stock returns 400."""
    user_headers = _register_and_login(client, "stock@test.com")
    product = _create_product(client, admin_headers, name="Limited Jersey", price=9999.99, stock=1)

    resp = client.post(
        "/orders/",
        json={"items": [{"product_id": product["id"], "quantity": 5}]},
        headers=user_headers,
    )
    assert resp.status_code == 400