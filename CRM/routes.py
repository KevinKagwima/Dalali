from flask import Blueprint, render_template, flash, url_for, redirect, request, make_response
from flask_login import login_required, current_user
from Models.base_model import db
from Models.lead import LeadClientDetails, Lead
from Models.properties import Property, PropertyLocation
from Dalali.routes import cache, CachedResponse
from .form import NewLeadForm
from decorators import role_required

crm = Blueprint("crm", __name__)

@crm.route("/leads")
@login_required
@role_required(["Dalali"])
def leads():
  form = NewLeadForm()
  form.property_listing.choices = [(listing.id, listing.name) for listing in Property.query.filter_by(owner_id=current_user.id).all()]

  context = {
    "form": form,
    "leads": Lead.query.filter_by(dalali_id=current_user.id).all()
  }

  return CachedResponse(
    response = make_response(
      render_template("Dalali/leads.html", **context)
    ),
    timeout=600
  )

@crm.route("/new-lead", methods=["POST"])
@login_required
@role_required(["Dalali"])
def add_new_lead():
  form = NewLeadForm()
  form.property_listing.choices = [(listing.id, listing.name) for listing in Property.query.filter_by(owner_id=current_user.id).all()]

  if form.validate_on_submit():
    try:
      cache.clear()
      new_lead_details = LeadClientDetails(
        first_name = form.first_name.data,
        last_name = form.last_name.data,
        email = form.email_address.data,
        phone = form.phone_number.data,
      )
      db.session.add(new_lead_details)
      db.session.commit()
      new_lead = Lead(
        property_id = form.property_listing.data,
        dalali_id = current_user.id,
        client_id = new_lead_details.id,
      )
      db.session.add(new_lead)
      db.session.commit()
      flash("Lead added successfully", "success")
      return redirect(url_for('crm.leads'))
    except Exception as e:
      db.session.rollback()
      flash(f"{str(e)}", "danger")
      return redirect(url_for('crm.leads'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
    return redirect(url_for("crm.leads"))

@crm.route("/close-leads/<int:lead_id>")
@login_required
@role_required(["Dalali"])
def close_lead(lead_id):
  try:
    cache.clear()
    lead = Lead.query.filter_by(unique_id=lead_id).first()
    if not lead:
      flash("Lead not found", "danger")
      return redirect(url_for('crm.leads'))
    lead.is_open = False
    lead.is_closed = True
    db.session.commit()
    flash("Lead closed successfully", "success")
    return redirect(url_for('crm.leads'))
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(url_for('crm.leads'))
