def test_create_allergen(client, test_dish):
    allergen = {
        "dish_id": test_dish["id"],
        "allergen": "Test allergen",
        "likelihood": 50,
    }

    response = client.post("/allergens", json=allergen)

    assert response.status_code == 201
    data = response.json()
    assert data["dish_id"] == allergen["dish_id"]
    assert data["allergen"] == allergen["allergen"]
    assert data["likelihood"] == allergen["likelihood"]
    assert "id" in data


def test_create_duplicate_allergen(client, test_dish):
    allergen = {
        "dish_id": test_dish["id"],
        "allergen": "Test allergen",
        "likelihood": 50,
    }

    response = client.post("/allergens", json=allergen)
    assert response.status_code == 201

    response2 = client.post("/allergens", json=allergen)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Allergen likelihood entry already exists"


def test_get_allergen(client, test_dish):
    allergen = {
        "dish_id": test_dish["id"],
        "allergen": "Test allergen",
        "likelihood": 50,
    }

    response = client.post("/allergens", json=allergen)
    assert response.status_code == 201
    data = response.json()

    response2 = client.get(f"/allergens/{data['id']}")
    assert response2.status_code == 200
    data2 = response2.json()

    assert data2["dish_id"] == allergen["dish_id"]
    assert data2["allergen"] == allergen["allergen"]
    assert data["likelihood"] == allergen["likelihood"]
    assert "id" in data2


def test_delete_allergen(client, test_dish):
    allergen = {
        "dish_id": test_dish["id"],
        "allergen": "Test allergen",
        "likelihood": 50,
    }

    response = client.post("/allergens", json=allergen)
    assert response.status_code == 201
    data = response.json()

    response2 = client.delete(f"/allergens/{data['id']}")
    assert response2.status_code == 204
