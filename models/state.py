#!/usr/bin/python3
"""This module defines a class for State"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """State class for storing state information"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """Return the list of City objects linked to the current State."""
        from models import storage  # Import here to avoid circular import
        from models.city import City
        return [city for city in storage.all(City).values() if city.state_id == self.id]
