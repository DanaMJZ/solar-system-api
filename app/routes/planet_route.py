from app.models.planet import Planet
from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from .route_utilities import validate_model

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
    discription_param = request.args.get("discription")
    distance_param = request.args.get("distance")
    if discription_param:
        query = query.where(Planet.discription == discription_param)
    if  distance_param:
        query = query.where(Planet.distance == int(distance_param))

    query = query.order_by(Planet.id.desc())       # building sql query, We use SQLAlchemy to send select formated request to our db to get all cats sorted by the order
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
    planet = validate_model(Planet,planet_id)
    request_body = request.get_json()
    planet = Planet.from_dict(request_body)
    # planet.name = request_body["name"]
    # planet.description = request_body["description"]
    # planet.distance = request_body["distance"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet,planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")




# @planets_bp.get("")
# def get_all_planets():
#     planets_response = []
#     for planet in planets:
#         planets_response.append(
#             {
#                 "id": planet.id,
#                 "name": planet.name,
#                 "description": planet.description
#             }
#         )
#     return planets_response

# @planets_bp.get("/<planet_id>")
# def get_one_planet(planet_id):
#     planet = validate_model(planet_id)

#     return {
#             "id": planet.id,
#             "name": planet.name,
#             "description": planet.description
#     }

    
# def validate_model(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         response = {"message": f"planet {planet_id} invalid"}
#         abort(make_response(response, 400))

#     for planet in planets:
#         if planet.id == planet_id:
#             return planet

#     response = {"message": f"planet {planet_id} not found"}
#     abort(make_response(response, 404))
