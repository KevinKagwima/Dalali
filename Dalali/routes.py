from flask import Blueprint, Flask, render_template, flash, url_for, redirect, request, make_response
from flask_login import login_required, current_user
from Models.base_model import db, get_local_time
from Models.properties import Property, PropertyTypes, PropertyLocation, PropertyAmenities, PropertyImages
from Models.ratings import Ratings
from .form import PropertyDetailsForm, AmenitiesForm, PropertyLocationForm
from .aws_credentials import awsCredentials
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from flask_caching import Cache, CachedResponse
from slugify import slugify
from decorators import role_required
from celery import Celery, Task
from Utils.tasks import upload_property_images
import boto3

dalali = Blueprint("dalali", __name__)
s3 = boto3.resource(
  "s3",
  aws_access_key_id = awsCredentials.aws_access_key,
  aws_secret_access_key = awsCredentials.aws_secret_key
)
bucket_name = awsCredentials.bucket_name
region = awsCredentials.region
cache = Cache()

VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
COMPRESS_SETTINGS = {
  'codec': 'libx264',
  'preset': 'medium',
  'crf': 28,
  'threads': 4
}

def celery_init_app(app: Flask) -> Celery:
  class FlaskTask(Task):
    def __call__(self, *args: object, **kwargs: object) -> object:
      with app.app_context():
        return self.run(*args, **kwargs)

  celery_app = Celery(app.name, task_cls=FlaskTask)
  celery_app.config_from_object(app.config["CELERY"])
  celery_app.set_default()
  app.extensions["celery"] = celery_app
  return celery_app

@dalali.route("/dashboard")
@login_required
@role_required(["Dalali"])
def dashboard():
  ratings = [rating.rating for rating in Ratings.query.filter_by(user_id=current_user.id).all()]
  if ratings:
    average_rating = (sum(ratings)/len(ratings))

  context = {
    "properties": Property.query.filter_by(owner_id=current_user.id).all(),
    "ratings": ratings,
    "average_rating": average_rating if ratings else 0,
  }

  return CachedResponse(
    response = make_response(
      render_template("Dalali/dashboard.html", **context)
    ),
    timeout=600
  )

@dalali.route("/upload/property", methods=["POST", "GET"])
@login_required
@role_required(["Dalali"])
def upload_property():
  form = PropertyDetailsForm()
  form.property_type_id.choices = [(property_type.id, property_type.name) for property_type in PropertyTypes.query.all()]

  if form.validate_on_submit():
    try:
      cache.clear()
      if not check_existing_property(form.name.data):
        flash(f"Property with name {form.name.data} already exists", "danger")
        return redirect(url_for('dalali.upload_property'))
      
      print()

      if form.property_type_id.data == "1" and not form.property_size.data:
        flash("You must submit property size", "warning")
        return redirect(url_for('dalali.upload_property'))

      else:
        new_property = Property(
          name = form.name.data,
          alias = slugify(form.name.data),
          description = form.description.data,
          rent = form.rent.data,
          currency = form.currency.data,
          property_type_id = form.property_type_id.data,
          auction_status = form.auction_status.data,
          owner_id = current_user.id,
        )
        db.session.add(new_property)
        db.session.commit()
        if form.property_size.data:
          new_property.property_size = form.property_size.data
          db.session.commit()
        flash("Property details saved successfully", "success")
        return redirect(url_for('dalali.upload_property_location', property_id=new_property.alias))
    except Exception as e:
      flash(f"{str(e)}. try again later", "danger")
      print(f"Error: {str(e)}")
      db.session.rollback()
      return redirect(url_for('dalali.upload_property'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
    return redirect(url_for('dalali.upload_property'))

  context = {
    "form": form
  }

  return CachedResponse(
    response = make_response(
      render_template("Dalali/upload-property-details.html", **context)
    ),
    timeout=600
  )

def check_existing_property(property_name):
  existing_property = Property.query.filter_by(name=property_name).first()
  if existing_property:
    return False
  else:
    return True

@dalali.route("/upload/property-location/<string:property_id>", methods=["POST", "GET"])
@login_required
@role_required(["Dalali"])
def upload_property_location(property_id):
  upload_property = Property.query.filter_by(alias=property_id).first()
  if not upload_property:
    flash("Property not found", "danger")
    return redirect(request.referrer)
  
  form = PropertyLocationForm()

  if form.validate_on_submit():
    try:
      cache.clear()
      new_location = PropertyLocation(
        region = form.region.data,
        district = form.district.data,
        town = form.town.data,
        house_no = form.house_no.data,
        street = form.street.data,
        landmark = form.landmark.data,
        property_id = upload_property.id
      )
      db.session.add(new_location)
      db.session.commit()
      flash(f"Location updated successfully", "success")
      return redirect(url_for('dalali.upload_property_amenities', property_id=upload_property.alias))

    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for('dalali.upload_property_location', property_id=upload_property.alias))

  context = {
    "form": form,
    "upload_property": upload_property
  }

  return CachedResponse(
    response = make_response(
      render_template("Dalali/upload-property-location.html", **context)
    ),
    timeout=600
  )

@dalali.route("/upload/property/amenities/<string:property_id>", methods=["POST", "GET"])
@login_required
@role_required(["Dalali"])
def upload_property_amenities(property_id):
  upload_property = Property.query.filter_by(alias=property_id).first()
  if not upload_property:
    flash("Property not found", "danger")
    return redirect(request.referrer)
  
  form = AmenitiesForm()

  if form.validate_on_submit():
    try:
      cache.clear()
      new_amenity = PropertyAmenities(
        name = form.name.data,
        property_id = upload_property.id
      )
      db.session.add(new_amenity)
      db.session.commit()
      flash(f"{new_amenity.name} added as an amenity", "success")
      return redirect(url_for('dalali.upload_property_amenities', property_id=upload_property.alias))

    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for('dalali.upload_property_amenities', property_id=upload_property.alias))

  context = {
    "form": form,
    "upload_property": upload_property
  }

  return CachedResponse(
    response = make_response(
      render_template("Dalali/upload-property-amenities.html", **context)
    ),
    timeout=600
  )

@dalali.route("/remove-amenity/<string:amenity_id>")
@login_required
@role_required(["Dalali"])
def remove_amenity(amenity_id):
  amenity = PropertyAmenities.query.filter_by(unique_id=amenity_id).first()
  if not amenity:
    flash("Amenity not found", category="danger")
    return redirect(request.referrer)
  try:
    cache.clear()
    db.session.delete(amenity)
    db.session.commit()
    flash("Amenity removed successfully", "success")
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

@dalali.route("/upload/property/images/<string:property_id>", methods=["POST", "GET"])
@login_required
@role_required(["Dalali"])
def upload_property_images(property_id):
  upload_property = Property.query.filter_by(alias=property_id).first()
  if not upload_property:
    flash("Property not found", "danger")
    return redirect(request.referrer)
  
  if request.method == "POST":
    try:
      cache.clear()
      files = request.files.getlist("images")
      if files:
        if len(files) > 5 or len(upload_property.property_images) > 5:
          flash("Maximum of 5 images allowed", "info")
          return redirect(url_for('dalali.upload_property_images', property_id=upload_property.alias))
        else:
          # upload_property_images.delay(upload_property.id, files)
          upload_file(upload_property.id, files)
        return redirect(url_for('dalali.dashboard'))
      else:
        flash("No images selected", "danger")
        return redirect(url_for('dalali.upload_property_images', property_id=upload_property.alias))
    except Exception as e:
      flash(f"{str(e)}", "danger")

  context = {
    "upload_property": upload_property
  }

  return CachedResponse(
    response = make_response(
      render_template("Dalali/upload-property-images.html", **context)
    ),
    timeout=600
  )

def upload_file(property_id, files):
  upload_property = Property.query.get(property_id)
  try:
    for file in files:
      filename = f"{upload_property.alias}/{file.filename}"
      filetype = file.filename.split(".")[-1]
      unit_image = PropertyImages(
        image_name = filename,
        property_id = upload_property.id,
        image_type = filetype
      )
      s3.Bucket(bucket_name).upload_fileobj(file, filename)
      db.session.add(unit_image)
      upload_property.is_published = True
      db.session.commit()
    flash("Images uploaded successfully", "success")
  except NoCredentialsError:
    db.session.rollback()
    flash("Credentials not available", "danger")
    return redirect(url_for('dalali.upload_property_images', property_id=upload_property.alias))
  except PartialCredentialsError:
    db.session.rollback()
    flash("Incomplete credentials provided", "danger")
    return redirect(url_for('dalali.upload_property_images', property_id=upload_property.alias))
  except ClientError as e:
    db.session.rollback()
    flash(f"Client Error: {e.response['Error']['Message']}", "danger")
    return redirect(url_for('dalali.upload_property_images', property_id=upload_property.alias))
  except Exception as e:
    db.session.rollback()
    flash(f"Error: {repr(e)}", "danger")
    return redirect(url_for('dalali.upload_property_images', property_id=upload_property.alias))

@dalali.route("/remove-image/<string:image_id>")
@login_required
@role_required(["Dalali"])
def remove_image(image_id):
  image = PropertyImages.query.filter_by(unique_id=image_id).first()
  if not image:
    flash("Amenity not found", category="danger")
    return redirect(request.referrer)
  try:
    cache.clear()
    s3.Bucket(bucket_name).Object(image.image_name).delete()
    db.session.delete(image)
    db.session.commit()
    flash("Image removed successfully", "success")
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

@dalali.route("/property-details/<string:property_id>")
@login_required
@role_required(["Dalali"])
def property_details(property_id):
  selected_property = Property.query.filter_by(alias=property_id).first()
  if not selected_property:
    flash("Property not found", "danger")
    return redirect(url_for('dalali.dashboard'))
  
  propDetailsForm = PropertyDetailsForm(obj=selected_property)
  propDetailsForm.property_type_id.choices = [(property_type.id, property_type.name) for property_type in PropertyTypes.query.all()]

  property_location = PropertyLocation.query.filter_by(property_id=selected_property.id).first()
  locationForm = PropertyLocationForm(obj=property_location)
  
  context = {
    "property": selected_property,
    "propDetailsForm": propDetailsForm,
    "locationForm": locationForm,
  }

  return CachedResponse(
    response = make_response(
      render_template("Dalali/property-details.html", **context)
    ),
    timeout=600
  )

@dalali.route("/update/property-details/<string:property_id>", methods=["POST"])
@login_required
@role_required(["Dalali"])
def update_property_details(property_id):
  try:
    cache.clear()
    selected_property = Property.query.filter_by(alias=property_id).first()
    if not selected_property:
      flash("Property not found", "danger")
      return redirect(url_for('dalali.dashboard'))
    
    propDetailsForm = PropertyDetailsForm()
    propDetailsForm.property_type_id.choices = [(property_type.id, property_type.name) for property_type in PropertyTypes.query.all()]

    if propDetailsForm.validate_on_submit():
      propDetailsForm.populate_obj(selected_property)
      selected_property.alias = slugify(propDetailsForm.name.data)
      db.session.commit()
      flash("Property details updated successfully", "success")
      return redirect(url_for("dalali.property_details", property_id=selected_property.alias))
    
    if propDetailsForm.errors != {}:
      for err_msg in propDetailsForm.errors.values():
        flash(f"{err_msg}", "danger")
      return redirect(url_for("dalali.property_details", property_id=selected_property.alias))

  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

@dalali.route("/update/property-location/<string:property_id>", methods=["POST"])
@login_required
@role_required(["Dalali"])
def update_property_location(property_id):
  try:
    cache.clear()
    selected_property = Property.query.filter_by(alias=property_id).first()
    if not selected_property:
      flash("Property not found", "danger")
      return redirect(url_for('dalali.dashboard'))
    
    property_location = PropertyLocation.query.filter_by(property_id=selected_property.id).first()
    locationForm = PropertyLocationForm()

    if locationForm.validate_on_submit():
      locationForm.populate_obj(property_location)
      db.session.commit()
      flash("Property location updated successfully", "success")
      return redirect(url_for("dalali.property_details", property_id=selected_property.alias))
    
    if locationForm.errors != {}:
      for err_msg in locationForm.errors.values():
        flash(f"{err_msg}", "danger")
      return redirect(url_for("dalali.property_details", property_id=selected_property.alias))

  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

@dalali.route("/remove-property/<string:property_id>")
@login_required
@role_required(["Dalali"])
def remove_property(property_id):
  selected_property = Property.query.filter_by(alias=property_id).first()
  if not selected_property:
    flash("Property not found", category="danger")
    return redirect(request.referrer)
  try:
    cache.clear()
    property_locations = PropertyLocation.query.filter_by(property_id=selected_property.id).all()
    if property_locations:
      for location in property_locations:
        db.session.delete(location)
        db.session.commit()
    
    property_amenities = PropertyAmenities.query.filter_by(property_id=selected_property.id).all()
    if property_amenities:
      for amenity in property_amenities:
        remove_amenity(amenity.unique_id)
    
    property_images = PropertyImages.query.filter_by(property_id=selected_property.id).all()
    if property_images:
      for image in property_images:
        remove_image(image.unique_id)

    db.session.delete(selected_property)
    db.session.commit()
    flash("Property removed successfully", "success")
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer) 
