from Models.base_model import db, BaseModel

class SiteVisits(BaseModel, db.Model):
  __tablename__ = "site_visits"
  date = db.Column(db.Date(), nullable=False)
  time = db.Column(db.Time(), nullable=False)
  user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
  property_id = db.Column(db.Integer(), db.ForeignKey("property.id"))
  is_active = db.Column(db.Boolean(), default=True)
  is_canceled = db.Column(db.Boolean(), default=False)
