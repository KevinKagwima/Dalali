from app import create_app
from Models.base_model import db
from Models.properties import *
from Models.transactions import *
from Models.users import Role
from Models.properties import PropertyTypes
from Models.ratings import *
from Models.wishlist import *
from Models.lead import *
from Models.bookings import *

app = create_app()

def drop_tables():
  print("Dropping tables...")
  db.drop_all()
  print("Tables Dropped")

def create_tables():
  print("Creating tables...")
  db.create_all()
  print("Tables Created")

def add_roles():
  roles = ["Admin", "Dalali", "Client"]
  for role in roles:
    new_role = Role(
      name = role
    )
    db.session.add(new_role)
    db.session.commit()
    print(f"Added role {new_role.name}")

def add_property_types():
  property_types = ["Bare Land", "Bedsitter", "Studio", "1 Bedroom", "2 Bedroom", "3 Bedroom", "4 Bedroom", "5 Bedroom"]
  for property_type in property_types:
    new_property_type = PropertyTypes(
      name = property_type
    )
    db.session.add(new_property_type)
    db.session.commit()
    print(f"Added property type: {new_property_type.name}")

if __name__ == "__main__":
  with app.app_context():
    drop_tables()
    create_tables()
    add_roles()
    add_property_types()
