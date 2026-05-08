from Models.base_model import db, BaseModel

class Wishlist(BaseModel, db.Model):
  __tablename__ = 'wishlist'
  property_id = db.Column(db.Integer(), db.ForeignKey("property.id", ondelete="SET NULL"))
  user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="SET NULL"))

  def __repr__(self):
    return f"{self.property_id}"
