#!/usr/bin/python3
"""This module defines a class for City"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """City class for storing city information"""
    __tablename__ = 'cities'

    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)

    # Relationship with Place
    places = relationship("Place", backref="cities", cascade="all, delete, delete-orphan")
