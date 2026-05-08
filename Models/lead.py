from Models.base_model import db, BaseModel

class LeadClientDetails(BaseModel, db.Model):
  __tablename__ = "lead_client_details"
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)
  phone = db.Column(db.Integer(), nullable=False, unique=True)
  lead = db.relationship("Lead", backref="user_lead", lazy=True, cascade="all, delete, delete-orphan", passive_deletes=True)

class Lead(BaseModel, db.Model):
  __tablename__ = "lead"
  dalali_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="SET NULL"))
  client_id = db.Column(db.Integer(), db.ForeignKey("lead_client_details.id", ondelete="SET NULL"))
  property_id = db.Column(db.Integer(), db.ForeignKey("property.id", ondelete="SET NULL"))
  is_open = db.Column(db.Boolean(), default=True)
  is_closed = db.Column(db.Boolean(), default=False)
