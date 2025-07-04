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
    assert (
        response2.json()["detail"]
        == "Allergen likelihood entry already exists for this dish"
    )


def test_get_allergen_likelihoods_by_dish_id(client):
    dish1 = {"name": "Dish One", "country": "Testland"}
    dish2 = {"name": "Dish Two", "country": "Elsewhere"}
    response1 = client.post("/dishes", json=dish1)
    response2 = client.post("/dishes", json=dish2)
    dish1_id = response1.json()["id"]
    dish2_id = response2.json()["id"]

    allergen1 = {"dish_id": dish1_id, "allergen": "Nuts", "likelihood": 60}
    allergen2 = {"dish_id": dish2_id, "allergen": "Gluten", "likelihood": 80}
    client.post("/allergens", json=allergen1)
    client.post("/allergens", json=allergen2)

    response = client.get(f"/allergens/by-dish/{dish1_id}")
    assert response.status_code == 200
    data = response.json()

    assert any(a["allergen"] == "Nuts" and a["dish_id"] == dish1_id for a in data)

    assert all(a["dish_id"] == dish1_id for a in data)
    assert all(a["allergen"] != "Gluten" for a in data)


def test_get_all_allergenes(client, test_dish):
    allergen1 = {
        "dish_id": test_dish["id"],
        "allergen": "Test allergen1",
        "likelihood": 60,
    }
    allergen2 = {
        "dish_id": test_dish["id"],
        "allergen": "Test allergen2",
        "likelihood": 70,
    }

    response1 = client.post("/allergens", json=allergen1)
    assert response1.status_code == 201
    response2 = client.post("/allergens", json=allergen2)
    assert response2.status_code == 201

    response3 = client.get("/allergens")
    assert response3.status_code == 200
    data = response3.json()

    assert any(
        a["allergen"] == "Test allergen1" and a["likelihood"] == 60 for a in data
    )
    assert any(
        a["allergen"] == "Test allergen2" and a["likelihood"] == 70 for a in data
    )
    for allergen in data:
        assert isinstance(allergen["id"], int)
        assert allergen["dish_id"] == test_dish["id"]


def test_get_allergen(client, test_dish):
    allergen = {
        "dish_id": test_dish["id"],
        "allergen": "Test allergen",
        "likelihood": 50,
    }

    response = client.post("/allergens", json=allergen)
    assert response.status_code == 201
    data = response.json()

    response2 = client.get(f"/allergens/id/{data['id']}")
    assert response2.status_code == 200
    data2 = response2.json()

    assert data2["dish_id"] == allergen["dish_id"]
    assert data2["allergen"] == allergen["allergen"]
    assert data2["likelihood"] == allergen["likelihood"]
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
