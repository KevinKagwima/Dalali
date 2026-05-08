from Models.base_model import db, BaseModel

class Ratings(BaseModel, db.Model):
  __tablename__ = 'ratings'
  rating = db.Column(db.Integer(), nullable=False)
  user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
  rated_by = db.Column(db.Integer())

  def __repr__(self):
    return f"{self.rating}"
