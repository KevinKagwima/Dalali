from Models.base_model import db, BaseModel
from .wishlist import Wishlist
from .lead import Lead

class PropertyTypes(BaseModel, db.Model):
  __tablename__ = 'property_types'
  name = db.Column(db.String(30), nullable=False)
  properties = db.relationship("Property", backref="property_types", lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)

  def __repr__(self):
    return f"{self.name}"

class Property(BaseModel, db.Model):
  __tablename__ = "property"
  name = db.Column(db.String(300), nullable=False)
  alias = db.Column(db.String(300), nullable=False)
  description = db.Column(db.Text())
  rent = db.Column(db.Integer(), nullable=False, default=0)
  currency = db.Column(db.String(3))
  property_size = db.Column(db.Integer(), default=0)
  property_type_id = db.Column(db.Integer(), db.ForeignKey("property_types.id"))
  auction_status = db.Column(db.String(5), nullable=False)
  is_published = db.Column(db.Boolean(), default=False)
  owner_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
  property_amenities = db.relationship("PropertyAmenities", backref="property_amenities", lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
  property_location = db.relationship("PropertyLocation", backref="property_location", lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
  property_images = db.relationship("PropertyImages", backref="property_images", lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
  wishlist = db.relationship("Wishlist", backref="property_wishlist", lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
  lead = db.relationship("Lead", backref="property_leads", lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
  bookings = db.relationship("SiteVisits", backref="property_bookings", lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)
  
  def __repr__(self):
    return f"{self.name}"

class PropertyAmenities(BaseModel, db.Model):
  __tablename__ = "property_amenities"
  name = db.Column(db.String(100), nullable=False)
  property_id = db.Column(db.Integer(), db.ForeignKey("property.id"))
  
  def __repr__(self):
    return f"{self.name}"

class PropertyLocation(BaseModel, db.Model):
  __tablename__ = "property_location"
  region = db.Column(db.String(100), nullable=False)
  district = db.Column(db.String(100), nullable=False)
  town = db.Column(db.String(100), nullable=False)
  house_no = db.Column(db.String(100))
  street = db.Column(db.String(100))
  landmark = db.Column(db.String(100))
  property_id = db.Column(db.Integer(), db.ForeignKey("property.id"))
  
  def __repr__(self):
    return f"{self.region}, {self.district}"

class PropertyImages(BaseModel, db.Model):
  __tablename__ = "property_images"
  image_name = db.Column(db.String(200), nullable=False)
  image_type = db.Column(db.String(10), nullable=False)
  property_id = db.Column(db.Integer(), db.ForeignKey("property.id"))
  
  def __repr__(self):
    return f"{self.image_name}"
