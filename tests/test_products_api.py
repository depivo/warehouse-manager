def create_sample(client, name="Хлеб", quantity=10):
    response = client.post("/products/", json={"name": name, "quantity": quantity})
    return response.json()


def test_create_product(client):
    response = client.post("/products/", json={"name": "Хлеб", "quantity": 10})

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Хлеб"


def test_create_product_rejects_negative_quantity(client):
    response = client.post("/products/", json={"name": "Хлеб", "quantity": -1})

    assert response.status_code == 422


def test_list_products(client):
    create_sample(client, "Хлеб")
    create_sample(client, "Молоко")

    response = client.get("/products/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_product_by_id(client):
    created = create_sample(client)

    response = client.get(f"/products/{created['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Хлеб"


def test_get_missing_product_returns_404(client):
    response = client.get("/products/999")

    assert response.status_code == 404


def test_update_product_keeps_unsent_fields(client):
    created = create_sample(client, quantity=10)

    response = client.put(f"/products/{created['id']}", json={"name": "Батон"})

    assert response.status_code == 200
    assert response.json()["name"] == "Батон"
    assert response.json()["quantity"] == 10


def test_update_missing_product_returns_404(client):
    response = client.put("/products/999", json={"name": "Батон"})

    assert response.status_code == 404


def test_delete_product(client):
    created = create_sample(client)

    response = client.delete(f"/products/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/products/{created['id']}").status_code == 404


def test_delete_missing_product_returns_404(client):
    response = client.delete("/products/999")

    assert response.status_code == 404
