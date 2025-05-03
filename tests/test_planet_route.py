import pytest
def test_create_planet_no_name(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid request: missing name"}

def test_create_one_planet_no_description(client):
    # Arrange
    test_data = {"name": "Planet X"}

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid request: missing description"}

def test_create_one_planet_with_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "Planet X",
        "description": "The Best!",
        "distance" : 0

    }

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    # Check that response has only expected keys
    assert set(response_body.keys()) == {"id", "name", "description", "distance"}
    assert response_body["name"] == "Planet X"
    assert response_body["description"] == "The Best!"
    assert response_body["distance"] == 0


def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_planet(client,two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Mercury",
        "description": "The closest planet to the Sun",
        "distance" : 123
    }

def test_create_one_planet(client):
    # Act
    response = client.post("/planets", json={
        "name": "New planet",
        "description": "The Best!",
        "distance": 1234
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "New planet",
        "description": "The Best!",
        "distance":1234
    }

def test_delete_planet_missing_record(client):
    # Act
    response = client.get("/planets/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": f"Planet 3 not found"}



def test_get_all_planets_with_two_records(client, two_saved_planets):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "name": "Mercury",
        "description": "The closest planet to the Sun",
        "distance" : 123
    }
    assert response_body[1] == {
        "id": 2,
        "name": "Venus",
        "description": "The hottest planet in our solar system",
        "distance" : 456
    }

def test_get_all_planets_with_name_query_matching_none(client, two_saved_planets):
    # Act
    data = {'name': 'Earth'}
    response = client.get("/planets", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_planets_with_name_query_matching_one(client, two_saved_planets):
    # Act
    data = {'name': 'Mercury'}
    response = client.get("/planets", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "name": "Mercury",
        "description": "The closest planet to the Sun",
        "distance" : 123
    }


def test_get_one_planet_missing_record(client, two_saved_planets):
    # Act
    response = client.get("/planets/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 3 not found"}


def test_get_one_planet_invalid_id(client, two_saved_planets):
    # Act
    response = client.get("/planets/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet cat invalid"}

def test_update_planet(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "Planet X",
        "description": "The Best!",
        "distance" : 0
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_with_extra_keys(client, two_saved_planets):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "Planet X",
        "description": "The Best!",
        "distance" : 0
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_missing_record(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "Planet X",
        "description": "The Best!",
        "distance" : 0
    }

    # Act
    response = client.put("/planets/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 3 not found"}

def test_update_planet_invalid_id(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "Planet X",
        "description": "The Best!",
        "distance" : 0
    }

    # Act
    response = client.put("/planets/cat", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet cat invalid"}

def test_delete_planet(client, two_saved_planets):
    # Act
    response = client.delete("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully deleted"

def test_delete_planet_missing_record(client, two_saved_planets):
    # Act
    response = client.delete("/planets/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 3 not found"}

def test_delete_planet_invalid_id(client, two_saved_planets):
    # Act
    response = client.delete("/planets/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet cat invalid"}


