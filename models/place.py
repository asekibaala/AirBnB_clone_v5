#!/usr/bin/python3
"""This module defines a class for Place"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


# Table for Many-To-Many relationship between Place and Amenity
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """Place class for storing place information"""
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relationship with Amenity for DBStorage
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)

    # Getter for FileStorage
    @property
    def amenities(self):
        """Getter for amenities in FileStorage"""
        from models import storage  # Import moved here to avoid circular import
        from models.amenity import Amenity
        return [amenity for amenity in storage.all(Amenity).values() if amenity.id in self.amenity_ids]

    @amenities.setter
    def amenities(self, obj):
        """Setter for amenities in FileStorage"""
        from models.amenity import Amenity
        if isinstance(obj, Amenity):
            if hasattr(self, 'amenity_ids'):
                self.amenity_ids.append(obj.id)
            else:
                self.amenity_ids = [obj.id]
