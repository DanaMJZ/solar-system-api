from app.models.planet import Planet
from flask import Blueprint, abort, make_response, request, Response
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    distance = request_body["distance"]
    new_planet = Planet(name=name, description=description, distance=distance)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "distance" : new_planet.distance
    }
    return response, 201

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
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "distance" : planet.distance  
            }
    )


    return planets_response

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        response = {"message": f"planet {planet_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)
    if not planet:
        response = {"message": f"planet {planet_id} not found"}
        abort(make_response(response, 404))
    return planet

@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance" : planet.distance
    }

@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.distance = request_body["distance"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
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
#     planet = validate_planet(planet_id)

#     return {
#             "id": planet.id,
#             "name": planet.name,
#             "description": planet.description
#     }

    
# def validate_planet(planet_id):
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
