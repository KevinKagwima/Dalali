from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, EmailField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Models.users import Users

class NewLeadForm(FlaskForm):
  first_name = StringField(label="First Name", validators=[DataRequired()])
  last_name = StringField(label="Last Name", validators=[DataRequired()])
  email_address = EmailField(label="Email Address", validators=[Email(message="Invalid Email"), DataRequired()])
  phone_number = StringField(label="Phone Number",validators=[Length(min=10, max=10, message="Invalid Phone Number"), DataRequired()])
  property_listing = SelectField(label="Property Listing", choices=[], validators=[DataRequired()])

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = phone_number_to_validate.data
    if phone_number[0] != str(0):
      raise ValidationError("Invalid phone number. Phone number must begin with 0")
    elif phone_number[1] != str(7) and phone_number[1] != str(1):
      raise ValidationError("Invalid phone number. Phone number must begin with 0 followed by 7 or 1")
