from app.models.planet import Planet
import pytest

def test_from_dict_returns_planet():
    # Arrange
    planet_data = {
        "name": "Planet X",
        "description": "The Best!",
        "distance" : 0
    }

    # Act
    new_planet = Planet.from_dict(planet_data)

    # Assert
    assert new_planet.name == "Planet X"
    assert new_planet.description == "The Best!"
    assert new_planet.distance == 0

def test_from_dict_with_no_name():
    # Arrange
    planet_data = {
        "description": "The Best!",
        "distance" : 0
    }

    # Act & Assert
    with pytest.raises(KeyError, match='name'):
        new_planet = Planet.from_dict(planet_data)

def test_from_dict_with_no_description():
    # Arrange
    planet_data = {
        "name": "Planet X",
        "distance" : 0
    }

    # Act & Assert
    with pytest.raises(KeyError, match = 'description'):
        new_planet = Planet.from_dict(planet_data)

def test_from_dict_with_extra_keys():
    # Arrange
    planet_data = {
        "extra": "some stuff",
        "name": "Planet X",
        "description": "The Best!",
        "distance" : 0
    }

    # Act
    new_planet = Planet.from_dict(planet_data)

    # Assert
    assert new_planet.name == "Planet X"
    assert new_planet.description == "The Best!"
    assert new_planet.distance == 0


def test_to_dict_no_missing_data():
    # Arrange
    test_data = Planet(id = 1,
                    name="Mercury",
                    description="The closest planet to the Sun",
                    distance=123)

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["name"] == "Mercury"
    assert result["description"] == "The closest planet to the Sun"
    assert result["distance"] == 123

def test_to_dict_missing_id():
    # Arrange
    test_data = Planet(name="Mercury",
                    description="The closest planet to the Sun",
                    distance=123 )

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] is None
    assert result["name"] == "Mercury"
    assert result["description"] == "The closest planet to the Sun"
    assert result["distance"] == 123

def test_to_dict_missing_name():
    # Arrange
    test_data = Planet(id=1,
                    description="The closest planet to the Sun",
                    distance=123)

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["name"] is None
    assert result["description"] == "The closest planet to the Sun"
    assert result["distance"] == 123

def test_to_dict_missing_description():
    # Arrange
    test_data = Planet(id = 1,
                    name="Mercury",
                    distance=123)

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["name"] == "Mercury"
    assert result["description"] is None
    assert result["distance"] == 123
