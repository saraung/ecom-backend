def test_create_product(client):
    response = client.post(
        "/products/",
        json={
            "name": "Football Jersey",
            "description": "Club edition",
            "price": 1999.99,
            "stock_quantity": 10,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Football Jersey"
    assert float(data["price"]) == 1999.99
    assert data["stock_quantity"] == 10


def test_get_product(client):
    create_resp = client.post(
        "/products/",
        json={
            "name": "Shin Guards",
            "description": "Professional",
            "price": 499.99,
            "stock_quantity": 25,
        },
    )
    product_id = create_resp.json()["id"]

    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Shin Guards"


def test_get_product_not_found(client):
    resp = client.get("/products/9999")
    assert resp.status_code == 404


def test_update_product(client):
    create_resp = client.post(
        "/products/",
        json={
            "name": "Old Boots",
            "description": "Basic",
            "price": 999.99,
            "stock_quantity": 5,
        },
    )
    product_id = create_resp.json()["id"]

    resp = client.put(
        f"/products/{product_id}",
        json={"name": "Pro Boots", "price": 1499.99},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Pro Boots"
    assert float(resp.json()["price"]) == 1499.99


def test_delete_product(client):
    create_resp = client.post(
        "/products/",
        json={
            "name": "Gloves",
            "description": "Keeper",
            "price": 299.99,
            "stock_quantity": 15,
        },
    )
    product_id = create_resp.json()["id"]

    resp = client.delete(f"/products/{product_id}")
    assert resp.status_code == 204

    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 404


def test_list_products(client):
    client.post(
        "/products/",
        json={
            "name": "Ball",
            "description": "Match ball",
            "price": 149.99,
            "stock_quantity": 100,
        },
    )
    resp = client.get("/products/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)