def test_create_order_flow(client):
    # create user
    user = client.post(
        "/users/",
        json={"email": "order@test.com", "password": "pass123"}
    ).json()

    # create product
    product = client.post(
        "/products/",
        json={
            "name": "Boots",
            "description": "Pro boots",
            "price": 4999.99,
            "stock_quantity": 5
        }
    ).json()

    # create order
    response = client.post(
        "/orders/",
        json={
            "user_id": user["id"],
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2
                }
            ]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user["id"]
    assert len(data["items"]) == 1