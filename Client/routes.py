from flask import Blueprint, render_template, flash, url_for, redirect, request, make_response, session
from flask_login import login_required, current_user
from Dalali.routes import cache, CachedResponse
from Models.base_model import db
from Models.properties import Property, PropertyLocation, PropertyTypes
from Models.ratings import Ratings
from Models.wishlist import Wishlist
from Models.bookings import SiteVisits
from datetime import datetime

client = Blueprint("client", __name__)

@client.route("/")
@client.route("/home")
@client.route("/properties")
def properties():
  query = Property.query.filter_by(is_published=True)
  page = request.args.get('page', 1, type=int)
  properties = query.paginate(page=page, per_page=15, error_out=False)

  next_url = url_for('client.properties', page=properties.next_num) if properties.has_next else None
  prev_url = url_for('client.properties', page=properties.prev_num) if properties.has_prev else None

  context = {
    "properties": properties,
    "property_locations": PropertyLocation.query.all(),
    "next_url": next_url,
    "prev_url": prev_url,
    "next_page_number": properties.next_num,
    "prev_page_number": properties.prev_num,
    "active_page_number": request.args.get('page'),
  }

  return CachedResponse(
    response = make_response(
      render_template("Client/home.html", **context)
    ),
    timeout=600
  )

@client.route("/search", methods=["POST"])
def search():
  try:
    cache.clear()
    session.clear()

    transaction_type = request.form.get('auction_status')
    property_type = request.form.get('property_type')
    location = request.form.get('location')

    session["transaction_type"] = transaction_type
    session["property_type"] = property_type
    session["location"] = location

    return redirect(url_for('client.search_results'))
  except Exception as e:
    flash(f"{repr(e)}", category="danger")
    return redirect(url_for('client.properties'))

@client.route("/search/results")
def search_results():
  try:
    transaction_type = session["transaction_type"]
    property_type = session["property_type"]
    location = session["location"]

    query = Property.query.join(PropertyLocation).join(PropertyTypes)

    if transaction_type:
      query = query.filter(Property.auction_status == transaction_type, Property.is_published == True)
      
    if property_type:
      query = query.filter(PropertyTypes.name.ilike(f'%{property_type}%'), Property.is_published == True)
    
    if location:
      query = query.filter(
        (PropertyLocation.region.ilike(f'%{location}%')) |
        (PropertyLocation.district.ilike(f'%{location}%')) |
        (PropertyLocation.town.ilike(f'%{location}%')), 
        Property.is_published == True
      )

    page = request.args.get('page', 1, type=int)
    results = query.paginate(page=page, per_page=15, error_out=False)
    results_count = query.count()

    next_url = url_for('client.search_results', page=results.next_num) if results.has_next else None
    prev_url = url_for('client.search_results', page=results.prev_num) if results.has_prev else None

    context = {
      "properties": results,
      "results_count": results_count,
      "property_locations": PropertyLocation.query.all(),
      "search_query": "Exists",
      "next_url": next_url,
      "prev_url": prev_url,
      "next_page_number": results.next_num,
      "prev_page_number": results.prev_num,
      "active_page_number": request.args.get('page'),
      "transaction_type": transaction_type,
      "property_type": property_type,
      "location": location,
    }

    return CachedResponse(
      response = make_response(
        render_template("Client/search-results.html", **context)
      ),
      timeout=600
    )

  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(url_for("client.properties"))

@client.route("/property/<string:property_id>")
def property_details(property_id):
  view_property = Property.query.filter_by(alias=property_id).first()
  if not view_property:
    flash("Property not found", "danger")
    return redirect(url_for("client.properties"))
  
  ratings = [rating.rating for rating in Ratings.query.filter_by(user_id=view_property.owner_id).all()]
  if ratings:
    average_rating = (sum(ratings)/len(ratings))

  context = {
    "property": view_property,
    "location": PropertyLocation.query.filter_by(property_id=view_property.id).first(),
    "ratings": ratings,
    "average_rating": average_rating if ratings else 0,
  }

  return CachedResponse(
    response = make_response(
      render_template("Client/property-detail.html", **context)
    ),
    timeout=600
  )

@client.route("/rating/<int:user_id>", methods=["POST"])
@login_required
def rating(user_id):
  try:
    if request.method == "POST":
      cache.clear()
      self_rating = Ratings.query.filter_by(user_id=current_user.id).first()
      if self_rating:
        flash("You cannot rate yourself", "info")
        return redirect(request.referrer)

      existing_rating = Ratings.query.filter_by(user_id=user_id, rated_by=current_user.id).first()
      if existing_rating:
        flash("You have already rated this dalali", "info")
        return redirect(request.referrer)

      rating = int(request.form.get("rating"))
      new_rating = Ratings(
        rating  = rating,
        user_id = user_id,
        rated_by = current_user.id
      )
      db.session.add(new_rating)
      db.session.commit()
      flash("Rating saved successfully", "success")
      return redirect(request.referrer)
  except ValueError:
    flash("Failed to convert rating to number", "danger")
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

@client.route("/add-to-favourites/<string:property_id>")
@login_required
def add_to_favourites(property_id):
  try:
    cache.clear()
    selected_property = Property.query.filter_by(alias=property_id).first()
    if not selected_property:
      flash("Property not found", "danger")
      return redirect(request.referrer)
    
    existing_wishlist = Wishlist.query.filter_by(property_id=selected_property.id).first()
    if existing_wishlist:
      flash("Property already added to favourites", "info")
    else:
      new_wishlist = Wishlist(
        property_id = selected_property.id,
        user_id = current_user.id
      )
      db.session.add(new_wishlist)
      db.session.commit()
      flash("Property added to favourites successfully", "success")
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

@client.route("/favourites")
@login_required
def favourites():
  context = {
    "wishlist": Wishlist.query.filter_by(user_id=current_user.id).all(),
    "locations": PropertyLocation.query.all(),
    "properties": Property.query.all(),
  }

  return CachedResponse(
    response = make_response(
      render_template("Client/favourites.html", **context)
    ),
    timeout=600
  )

@client.route("/remove-favourite/<int:wishlist_id>")
@login_required
def remove_favourites(wishlist_id):
  try:
    cache.clear()
    wishlist = Wishlist.query.filter_by(unique_id=wishlist_id).first()
    if not wishlist:
      flash("Property not found favourites", "danger")
    else:
      db.session.delete(wishlist)
      db.session.commit()
      flash("Property removed from favourites", "success")
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

@client.route("/book/<string:property_id>", methods=["POST"])
@login_required
def create_booking(property_id):
  try:
    cache.clear()
    selected_property = Property.query.filter_by(alias=property_id).first()
    if not selected_property:
      flash("Property not found", "success")
      return redirect(request.referrer)
    
    date = request.form.get("date")
    time = request.form.get("time")

    if validate_booking(date, time, selected_property.id):
      new_booking = SiteVisits(
        date = date,
        time = time,
        user_id = current_user.id,
        property_id = selected_property.id,
      )
      db.session.add(new_booking)
      db.session.commit()
      flash("Booking created successfully", "success")
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

def validate_booking(date, time, property_id):
  booking = SiteVisits.query.filter_by(date=date, property_id=property_id, is_active=True).first()
  if booking:
    booking_time = datetime.strptime(booking.time.strftime("%H:%M"), "%H:%M")
    new_time = datetime.strptime(time, "%H:%M")
    diff = new_time - booking_time
    print(diff)
    return False
  else:
    return True
