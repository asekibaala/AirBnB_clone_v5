#!/usr/bin/python3
"""Test script for Place and Amenity relationship"""
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity

# Create a State
state = State(name="California")
state.save()

# Create a City
city = City(state_id=state.id, name="San Francisco")
city.save()

# Create a User
user = User(email="bob@hbtn.io", password="bobpwd", first_name="Bob", last_name="Dylan")
user.save()

# Create Places
place_1 = Place(user_id=user.id, city_id=city.id, name="Lovely Place")
place_1.save()
place_2 = Place(user_id=user.id, city_id=city.id, name="Awesome Spot")
place_2.save()

# Create Amenities
amenity_1 = Amenity(name="Wifi")
amenity_1.save()
amenity_2 = Amenity(name="Cable")
amenity_2.save()
amenity_3 = Amenity(name="Oven")
amenity_3.save()

# Link place_1 with 2 amenities
place_1.amenities.append(amenity_1)
place_1.amenities.append(amenity_2)

# Link place_2 with 3 amenities
place_2.amenities.append(amenity_1)
place_2.amenities.append(amenity_2)
place_2.amenities.append(amenity_3)

storage.save()

print("OK")
