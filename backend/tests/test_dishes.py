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


def test_get_all_dishes(client):
    dish1 = {"name": "Test dish1", "country": "Testland"}
    dish2 = {"name": "Test dish2", "country": "Testland2"}

    response1 = client.post("/dishes", json=dish1)
    assert response1.status_code == 201
    response2 = client.post("/dishes", json=dish2)
    assert response2.status_code == 201

    response3 = client.get("/dishes")
    assert response3.status_code == 200
    data = response3.json()

    names = [dish["name"] for dish in data]
    assert "Test dish1" in names
    assert "Test dish2" in names
    for dish in data:
        if dish["name"] == "Test dish1":
            assert dish["country"] == "Testland"
            assert isinstance(dish["id"], int)
        elif dish["name"] == "Test dish2":
            assert dish["country"] == "Testland2"
            assert isinstance(dish["id"], int)


def test_search_dish(client):
    dish = {"name": "Test dish", "country": "Testland"}

    response = client.post("/dishes", json=dish)
    assert response.status_code == 201

    query = "dish"
    response2 = client.get(f"/dishes/search?query={query}")
    assert response2.status_code == 200
    data = response2.json()

    assert any(
        d["name"] == "Test dish"
        and d["country"] == "Testland"
        and isinstance(d["id"], int)
        for d in data
    )


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
