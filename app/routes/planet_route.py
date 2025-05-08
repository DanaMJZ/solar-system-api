from app.models.planet import Planet
from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from .route_utilities import validate_model
from app.models.moon import Moon


planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")



@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    try:
        new_planet = Planet.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_planet)
    db.session.commit()
    return new_planet.to_dict(), 201



@planets_bp.get("")
def get_all_planets():
    query = db.select(Planet)
    name_param = request.args.get("name")
    description_param = request.args.get("description")
    distance_param = request.args.get("distance")
    if name_param:
        query = query.where(Planet.name == name_param)
    if description_param:
        query = query.where(Planet.discription == description_param)
    if  distance_param:
        query = query.where(Planet.distance == int(distance_param))

    query = query.order_by(Planet.id)       # building sql query, We use SQLAlchemy to send select formated request to our db to get all cats sorted by the order
    planets = db.session.scalars(query)
    planets_response = []
    for planet in planets:
        planets_response.append(planet.to_dict())
    return planets_response



@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(Planet,planet_id)
    return planet.to_dict()



@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()
    planet.name = request_body.get("name", planet.name)
    planet.description = request_body.get("description", planet.description)
    planet.distance = request_body.get("distance", planet.distance)
    # planet = Planet.from_dict(request_body)
    db.session.commit()
    return make_response(f'"Planet #{planet.id} successfully updated"', 200, {"Content-Type": "application/json"})

    # return Response(status=200, mimetype="application/json")



@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet,planet_id)
    db.session.delete(planet)
    db.session.commit()
    return make_response(f'"Planet #{planet.id} successfully deleted"', 200, {"Content-Type": "application/json"})

    # return Response(status=204, mimetype="application/json")

@planets_bp.post("/<planet_id>/moons")
def create_planet_with_moon(planet_id):
    planet = validate_model(Planet, planet_id)
    
    request_body = request.get_json()
    request_body["planet_id"] = planet.id

    try:
        new_moon = Moon.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
        
    db.session.add(new_moon)
    db.session.commit()

    return make_response(new_moon.to_dict(), 201) 

@planets_bp.get("/<planet_id>/moons")
def get_moons_by_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    response = [moon.to_dict() for moon in planet.moon]
    return response




