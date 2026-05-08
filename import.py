from flask import Flask
from Models.base_model import db
from Models.users import Role, Users
from Models.properties import *
from config import Config
import csv

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def add_roles():
  try:
    f = open("Data/roles.csv")
    reader = csv.reader(f)
    for name in reader:
      new_role = Role(
        name = name,
      )
      db.session.add(new_role)
      db.session.commit()
    print("Added all roles...")
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

def add_users():
  try:
    f = open("Data/users.csv")
    reader = csv.reader(f)
    for role_id, user_id, unique_id, first_name, last_name, email, phone, password in reader:
      new_user = Users(
        role_id = role_id,
        id = user_id,
        unique_id = unique_id,
        first_name = first_name,
        last_name = last_name,
        email = email,
        phone = phone,
        password = password
      )
      db.session.add(new_user)
      db.session.commit()
    print("Added all users...")
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

def add_property_types():
  try:
    f = open("Data/property_types.csv")
    reader = csv.reader(f)
    for name, prop_id, unique_id in reader:
      new_property_type = PropertyTypes(
        name = name,
        id = prop_id,
        unique_id = unique_id,
      )
      db.session.add(new_property_type)
      db.session.commit()
    print("Added all property types...")
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

def add_properties():
  try:
    f = open("Data/properties.csv")
    reader = csv.reader(f)
    for name, alias, description, rent, property_type_id, auction_status, owner_id, prop_id, unique_id in reader:
      new_property = Property(
        id = prop_id,
        name = name,
        alias = alias,
        unique_id = unique_id,
        description=description,
        rent=rent,
        property_type_id=property_type_id,
        auction_status=auction_status,
        is_published = True,
        owner_id=owner_id
      )
      db.session.add(new_property)
      db.session.commit()
    print("Added all properties...")
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

def add_property_location():
  try:
    f = open("Data/location.csv")
    reader = csv.reader(f)
    for region, district, town, house_no, street, landmark, id, prop_id, unique_id in reader:
      property_location = PropertyLocation(
        region = region,
        district = district,
        town = town,
        house_no = house_no,
        street = street,
        landmark = landmark,
        property_id = prop_id,
        id = id,
        unique_id = unique_id
      )
      db.session.add(property_location)
      db.session.commit()
    print("Added all property locations...")
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

def add_property_images():
  try:
    f = open("Data/images.csv")
    reader = csv.reader(f)
    for image_name, image_type, prop_id,id, unique_id in reader:
      property_images = PropertyImages(
        property_id = prop_id,
        unique_id = unique_id,
        image_name = image_name,
        image_type = image_type,
        id=id
      )
      db.session.add(property_images)
      db.session.commit()
    print("Added all property images...")
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

def add_property_amenities():
  try:
    f = open("Data/amenities.csv")
    reader = csv.reader(f)
    for name, prop_id, id, unique_id in reader:
      property_amenities = PropertyAmenities(
        property_id = prop_id,
        unique_id = unique_id,
        id=id,
        name = name
      )
      db.session.add(property_amenities)
      db.session.commit()
    print("Added all property amenities...")
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

if __name__ == "__main__":
  with app.app_context():
    # add_roles()
    # add_property_types()
    add_property_location()
    # add_property_images()
    # add_property_amenities()
    # add_users()
    # add_properties()
