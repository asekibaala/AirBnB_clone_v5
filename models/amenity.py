#!/usr/bin/python3
"""This module defines a class for Amenity"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity class for storing amenity information"""
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    # Relationship with Place through place_amenity
    place_amenities = relationship("Place", secondary="place_amenity", viewonly=True)
