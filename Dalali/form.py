from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

class PropertyDetailsForm(FlaskForm):
  name = StringField('Property Name', validators=[DataRequired(message="Property name field required"), Length(max=300)])
  description = TextAreaField('Property Description (Optional)', validators=[Optional()])
  rent = IntegerField('Rent/Sale Amount ', validators=[DataRequired(message="Property rent/sale field required")])
  currency = SelectField('Currency', choices=[("---", "Select Currency"), ("KSH", "KSH"), ("USD", "USD")],  validators=[DataRequired(message="Currency field required"), Length(min=3, max=3, message="Invalid Currency")])
  property_type_id = SelectField('Property Type', choices=[], validators=[DataRequired(message="Property Field field required")])
  property_size = IntegerField('Land Size (Optional)', validators=[Optional()])
  auction_status = SelectField('Rent/Sale', choices=["---", "Rent", "Sale"], validators=[DataRequired(message="Property auction type field required")])

class PropertyLocationForm(FlaskForm):
  region = StringField('Region', validators=[DataRequired(message="Region field required"), Length(max=50)])
  district = StringField('District', validators=[DataRequired(message="District field required"), Length(max=50)])
  town = StringField('Town', validators=[DataRequired(message="Town field required"), Length(max=50)])
  house_no = StringField('House No/Apartment No (Optional)', validators=[Optional(), Length(max=100)])
  landmark = StringField('Landmark', validators=[Optional(), Length(max=100)])
  street = StringField('Street', validators=[Optional(), Length(max=100)])

class AmenitiesForm(FlaskForm):
  name = StringField('Amenity', validators=[DataRequired(message="Amenities field required"), Length(max=100)])
