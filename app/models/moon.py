from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import ForeignKey
# from typing import Optional
from ..db import db

class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    size: Mapped[int]
    color: Mapped[str]
    description: Mapped[str]
    moons: Mapped[list["Planet"]] = relationship(back_populates="moon")

    def to_dict(self):
        moon_as_dict = {}
        moon_as_dict["id"] = self.id
        moon_as_dict["name"] = self.name
        moon_as_dict["size"] = self.size
        moon_as_dict["color"] = self.color
        moon_as_dict["description"] = self.description

        return moon_as_dict
    
    @classmethod
    def from_dict(cls, moon_data):
        # Use get() to fetch values that could be undefined to avoid raising an error


        new_moon = cls(
            name=moon_data["name"],
            size=moon_data["size"],
            color=moon_data["color"],
            description=moon_data["description"]
        )

        return new_moon