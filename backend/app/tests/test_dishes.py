def test_create_dish(client):
    dish = {"name": "Test dish", "country": "Testland"}

    response = client.post("/dishes", json=dish)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == dish["name"]
    assert data["country"] == dish["country"]
    assert "id" in data


def test_create_duplicate_dish(client):
    dish = {"name": "Test dish", "country": "Testland"}

    response = client.post("/dishes", json=dish)
    assert response.status_code == 201

    response2 = client.post("/dishes", json=dish)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Dish already exists"


def test_get_dish(client):
    dish = {"name": "Test dish", "country": "Testland"}

    response = client.post("/dishes", json=dish)
    assert response.status_code == 201
    data = response.json()

    response2 = client.get(f"/dishes/{data['id']}")
    assert response2.status_code == 200
    data2 = response2.json()

    assert data2["name"] == dish["name"]
    assert data2["country"] == dish["country"]
    assert "id" in data2


def test_delete_dish(client):
    dish = {"name": "Test dish", "country": "Testland"}

    response = client.post("/dishes", json=dish)
    assert response.status_code == 201
    data = response.json()

    response2 = client.delete(f"/dishes/{data['id']}")
    assert response2.status_code == 204
