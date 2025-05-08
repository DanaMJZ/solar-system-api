# class Planet:
#     def __init__(self, id, name, description):
#         self.id = id
#         self.name = name
#         self.description = description

# planets = [
#     Planet(1, "Mercury", "The closest planet to the Sun, the smallest with heavily cratered surface."), 
#     Planet(2, "Venus", "The hottest planet in our solar system, with a thick, toxic atmosphere"),
#     Planet(3, "Earth", "The third planet from the Sun, and the only known planet to support life."),
#     Planet(4, "Mars", "Known as the Red Planet due to its iron-rich soil, it has polar ice caps and canyons."),
#     Planet(5, "Jupiter", "The largest planet in our solar system, with a prominent Great Red Spot (a giant storm)."),
#     Planet(6, "Saturn", "Famous for its prominent ring system, composed of ice and rock particles."),
#     Planet(7, "Uranus", "A gas giant with a unique tilt, often called the icy giant."),
#     Planet(8, "Neptune", "The furthest planet from the Sun, also considered an icy giant.")
# ]

from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..db import db


#only when make changes related to database (change column) in model need to run migrate again. 
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    distance : Mapped[int]
    moons: Mapped[list["Moon"]] = relationship(back_populates="planet")

    @classmethod
    def from_dict(cls, planet_data):
        new_planet = Planet(name=planet_data["name"],
                        description=planet_data["description"],
                        distance = planet_data["distance"])
        return new_planet
    
    def to_dict(self):
        planet_as_dict = {}
        planet_as_dict["id"] = self.id
        planet_as_dict["name"] = self.name
        planet_as_dict["description"] = self.description
        planet_as_dict["distance"] = self.distance

        if self.moons:
            planet_as_dict["moons"] = [moon.name for moon in self.moons]

        return planet_as_dict
