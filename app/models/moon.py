from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import ForeignKey
# from typing import Optional
from ..db import db
from sqlalchemy import ForeignKey
from typing import Optional

class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    size: Mapped[int]
    color: Mapped[str]
    description: Mapped[str]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="moons")

    def to_dict(self):
        moon_as_dict = {}
        moon_as_dict["id"] = self.id
        moon_as_dict["name"] = self.name
        moon_as_dict["size"] = self.size
        moon_as_dict["color"] = self.color
        moon_as_dict["description"] = self.description

        if self.planet:
            moon_as_dict["planet"] = self.planet.name

        return moon_as_dict
    
    @classmethod
    def from_dict(cls, moon_data):
        # Use get() to fetch values that could be undefined to avoid raising an error
        planet_id = moon_data.get("planet_id")

        new_moon = cls(
            name=moon_data["name"],
            size=moon_data["size"],
            color=moon_data["color"],
            description=moon_data["description"],
            planet_id=planet_id
        )

        return new_moon