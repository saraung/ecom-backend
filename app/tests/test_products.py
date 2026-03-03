def test_create_product(client):
    response = client.post(
        "/products/",
        json={
            "name": "Football Jersey",
            "description": "Club edition",
            "price": 1999.99,
            "stock_quantity": 10
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Football Jersey"
    assert float(data["price"]) == 1999.99