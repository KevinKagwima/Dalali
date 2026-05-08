from flask import Blueprint, render_template, flash, url_for, redirect, request, make_response
from flask_login import login_user, login_required, logout_user
from Models.base_model import db
from Models.users import Users, Role
from flask_bcrypt import generate_password_hash
from Dalali.routes import cache, CachedResponse
from .form import UserRegistrationForm, UserLoginForm, ResetPasswordForm

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/dalali/signup", methods=["POST", "GET"])
def dalali_signup():
  form = UserRegistrationForm()
  if form.validate_on_submit():
    try:
      cache.clear()
      user = Users(
        first_name = form.first_name.data,
        last_name = form.last_name.data,
        email = form.email_address.data,
        phone = form.phone_number.data,
        role_id = Role.query.filter_by(name="Dalali").first().id,
        passwords = form.password.data,
      )
      db.session.add(user)
      db.session.commit()
      flash(f"Account created successfully", "success")
      return redirect(url_for("auth.signin"))
    
    except Exception as e:
      flash(f"{repr(e)}", "danger")
      return redirect(url_for("auth.dalali_signup"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
    return redirect(url_for("auth.dalali_signup"))

  context = {
    "form": form,
  }

  return CachedResponse(
    response = make_response(
      render_template("Auth/dalali-signup.html", **context)
    ),
    timeout=600
  )

@auth.route("/signup", methods=["POST", "GET"])
def client_signup():
  form = UserRegistrationForm()
  if form.validate_on_submit():
    try:
      cache.clear()
      user = Users(
        first_name = form.first_name.data,
        last_name = form.last_name.data,
        email = form.email_address.data,
        phone = form.phone_number.data,
        role_id = Role.query.filter_by(name="Client").first().id,
        passwords = form.password.data,
      )
      db.session.add(user)
      db.session.commit()
      flash(f"Account created successfully", "success")
      return redirect(url_for("auth.signin"))
    
    except Exception as e:
      flash(f"{repr(e)}", "danger")
      return redirect(url_for("auth.client_signup"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
    return redirect(url_for("auth.client_signup"))

  context = {
    "form": form,
  }

  return CachedResponse(
    response = make_response(
      render_template("Auth/signup.html", **context)
    ),
    timeout=600
  )

@auth.route("/signin", methods=["POST", "GET"])
def signin():
  form = UserLoginForm()
  if form.validate_on_submit():
    try:
      cache.clear()
      user = Users.query.filter_by(email=form.email_address.data).first()
      if not user:
        flash(f"No user with that email", "danger")
        return redirect(url_for("auth.signin"))
      elif user and user.check_password_correction(attempted_password=form.password.data):
        login_user(user, remember=True)
        flash(f"Login successfull", "success",)
        if user.user_role.name == "Dalali":
          return redirect(url_for("dalali.dashboard"))
        elif user.user_role.name == "Client":
          return redirect(url_for("client.properties"))
        else:
          return redirect(next or url_for("main.index"))
      else:
        flash(f"Invalid login credentials", "danger")
        return redirect(url_for("auth.signin"))

    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for('auth.signin'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
    return redirect(url_for("auth.signin"))
  
  context = {
    "form": form
  }

  return CachedResponse(
    response = make_response(
      render_template("Auth/signin.html", **context)
    ),
    timeout=600
  )

@auth.route("/reset-password", methods=["POST", "GET"])
def reset_password():
  form = ResetPasswordForm()
  if form.validate_on_submit():
    try:
      cache.clear()
      user = Users.query.filter_by(email=form.email_address.data).first()
      if user:
        if user.check_password_correction(attempted_password=form.password.data):
          flash("New password cannot be same as old", "danger")
          return redirect(url_for('auth.reset_password'))
        else:
          user.password = generate_password_hash(form.password.data).decode("utf-8")
          db.session.commit()
          flash("Your password has been reset successfully", "success")
          return redirect(url_for("auth.signin"))
      else:
        flash("No user with that email", "danger")
        return redirect(url_for('auth.reset_password'))

    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for('auth.reset_password'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
    return redirect(url_for('auth.reset_password'))

  context = {
    "form": form
  }

  return CachedResponse(
    response = make_response(
      render_template("Auth/reset-password.html", **context)
    ),
    timeout=600
  )

@auth.route("/logout")
@login_required
def logout():
  try:
    cache.clear()
    logout_user()
    flash(f"Logged out successfully!", "success")
  except Exception as e: 
    flash(f"Failed to Logged. Try again later", "danger")
  return redirect(url_for("auth.signin"))
