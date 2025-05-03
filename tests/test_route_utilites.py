from werkzeug.exceptions import HTTPException
from app.routes import validate_planet
import pytest
from app.models.planet import Planet
...

def test_validate_planet(two_saved_planets):
    # Act
    result_planet = validate_planet(Planet, 1)

    # Assert
    assert result_planet.id == 1
    assert result_planet.name == "Mercury"
    assert result_planet.description == "The closest planet to the Sun"
    assert result_planet.distance == 123

def test_validate_planet_missing_record(two_saved_planets):
    
    with pytest.raises(HTTPException):
        result_planet = validate_planet(Planet, "3")
    
def test_validate_planet_invalid_id(two_saved_planets):
    
    with pytest.raises(HTTPException):
        result_planet = validate_planet(Planet, "cat")