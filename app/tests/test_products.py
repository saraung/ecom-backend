from app.tests.conftest import _register_and_login, _make_superuser


def test_list_products_public(client):
    """Anyone can list products without auth."""
    resp = client.get("/products/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_product_public(client, admin_headers):
    """Anyone can view a product without auth."""
    # create as admin
    create_resp = client.post(
        "/products/",
        json={
            "name": "Public Boot",
            "description": "Visible to all",
            "price": 499.99,
            "stock_quantity": 25,
        },
        headers=admin_headers,
    )
    product_id = create_resp.json()["id"]
    # fetch without auth
    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Public Boot"


def test_get_product_not_found(client):
    resp = client.get("/products/9999")
    assert resp.status_code == 404


def test_create_product_as_admin(client, admin_headers):
    """Superuser can create products."""
    response = client.post(
        "/products/",
        json={
            "name": "Football Jersey",
            "description": "Club edition",
            "price": 1999.99,
            "stock_quantity": 10,
        },
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Football Jersey"
    assert float(data["price"]) == 1999.99
    assert data["stock_quantity"] == 10


def test_create_product_unauthorized(client):
    """Anonymous user gets 401."""
    resp = client.post(
        "/products/",
        json={
            "name": "Anon Product",
            "price": 100.0,
            "stock_quantity": 1,
        },
    )
    assert resp.status_code == 401


def test_create_product_forbidden(client, auth_headers):
    """Regular user gets 403."""
    resp = client.post(
        "/products/",
        json={
            "name": "Forbidden Product",
            "price": 100.0,
            "stock_quantity": 1,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 403


def test_update_product_as_admin(client, admin_headers):
    """Superuser can update products."""
    create_resp = client.post(
        "/products/",
        json={
            "name": "Old Boots",
            "description": "Basic",
            "price": 999.99,
            "stock_quantity": 5,
        },
        headers=admin_headers,
    )
    product_id = create_resp.json()["id"]

    resp = client.put(
        f"/products/{product_id}",
        json={"name": "Pro Boots", "price": 1499.99},
        headers=admin_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Pro Boots"
    assert float(resp.json()["price"]) == 1499.99


def test_update_product_forbidden(client, auth_headers, admin_headers):
    """Regular user cannot update products."""
    create_resp = client.post(
        "/products/",
        json={
            "name": "Guard Boot",
            "price": 100.0,
            "stock_quantity": 1,
        },
        headers=admin_headers,
    )
    product_id = create_resp.json()["id"]
    resp = client.put(
        f"/products/{product_id}",
        json={"name": "Hacked"},
        headers=auth_headers,
    )
    assert resp.status_code == 403


def test_delete_product_as_admin(client, admin_headers):
    """Superuser can delete products."""
    create_resp = client.post(
        "/products/",
        json={
            "name": "Gloves",
            "description": "Keeper",
            "price": 299.99,
            "stock_quantity": 15,
        },
        headers=admin_headers,
    )
    product_id = create_resp.json()["id"]
    resp = client.delete(f"/products/{product_id}", headers=admin_headers)
    assert resp.status_code == 204
    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 404


def test_delete_product_forbidden(client, auth_headers, admin_headers):
    """Regular user cannot delete products."""
    create_resp = client.post(
        "/products/",
        json={
            "name": "Protected",
            "price": 50.0,
            "stock_quantity": 1,
        },
        headers=admin_headers,
    )
    product_id = create_resp.json()["id"]
    resp = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert resp.status_code == 403