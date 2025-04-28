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

from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
#only when make changes related to database (change column) in model need to run migrate again. 
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
