def test_create_order_flow(client):
    # create user
    user = client.post(
        "/users/",
        json={"email": "order@test.com", "password": "pass123"},
    ).json()

    # create product
    product = client.post(
        "/products/",
        json={
            "name": "Boots",
            "description": "Pro boots",
            "price": 4999.99,
            "stock_quantity": 5,
        },
    ).json()

    # create order — total_amount is auto-calculated from product prices
    response = client.post(
        f"/orders/?user_id={user['id']}",
        json={
            "items": [
                {"product_id": product["id"], "quantity": 2}
            ]
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user["id"]
    assert len(data["items"]) == 1
    assert float(data["total_amount"]) == 4999.99 * 2


def test_get_order(client):
    user = client.post(
        "/users/",
        json={"email": "getorder@test.com", "password": "pass123"},
    ).json()

    product = client.post(
        "/products/",
        json={
            "name": "Jersey",
            "description": "Away kit",
            "price": 1999.99,
            "stock_quantity": 10,
        },
    ).json()

    order = client.post(
        f"/orders/?user_id={user['id']}",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
    ).json()

    resp = client.get(f"/orders/{order['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == order["id"]


def test_get_order_not_found(client):
    resp = client.get("/orders/9999")
    assert resp.status_code == 404


def test_delete_order(client):
    user = client.post(
        "/users/",
        json={"email": "delorder@test.com", "password": "pass123"},
    ).json()

    product = client.post(
        "/products/",
        json={
            "name": "Socks",
            "description": "Match socks",
            "price": 199.99,
            "stock_quantity": 50,
        },
    ).json()

    order = client.post(
        f"/orders/?user_id={user['id']}",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
    ).json()

    resp = client.delete(f"/orders/{order['id']}")
    assert resp.status_code == 204

    resp = client.get(f"/orders/{order['id']}")
    assert resp.status_code == 404


def test_insufficient_stock(client):
    user = client.post(
        "/users/",
        json={"email": "stock@test.com", "password": "pass123"},
    ).json()

    product = client.post(
        "/products/",
        json={
            "name": "Limited Jersey",
            "description": "Rare",
            "price": 9999.99,
            "stock_quantity": 1,
        },
    ).json()

    resp = client.post(
        f"/orders/?user_id={user['id']}",
        json={"items": [{"product_id": product["id"], "quantity": 5}]},
    )
    assert resp.status_code == 400