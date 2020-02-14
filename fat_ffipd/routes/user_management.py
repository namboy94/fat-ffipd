import os
from flask import Blueprint, redirect, url_for, request, render_template, flash
from flask_login import login_required, current_user, logout_user, login_user
from puffotter.crypto import verify_password, generate_hash, generate_random
from puffotter.recaptcha import verify_recaptcha
from puffotter.smtp import send_email
from fat_ffipd.flask import app, db
from fat_ffipd.config import Config
from fat_ffipd.db.auth.User import User

user_management_blueprint = Blueprint("user_management", __name__)


@user_management_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """
    Page that allows the user to log in
    :return: The response
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        remember_me = request.form.get("remember_me") in ["on", True]

        existing = {user.username: user for user in User.query.all()}
        user: User = existing.get(username)

        if user is None:
            flash("User does not exist", "danger")
        elif current_user.is_authenticated:
            flash("User already logged In", "info")
        elif not user.confirmed:
            flash("User is not confirmed", "danger")
        elif not verify_password(password, user.password_hash):
            flash("Invalid Password", "danger")
        else:
            login_user(user, remember=remember_me)
            flash("Logged in successfully", "success")
            return redirect(url_for("static.index"))
        return redirect(url_for("user_management.login"))
    else:
        return render_template("profile/login.html")


@user_management_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Logs out the user
    :return: The response
    """
    logout_user()
    app.logger.info("User {} logged out.".format(current_user.username))
    flash("Logged out", "info")
    return redirect(url_for("static.index"))


@user_management_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """
    Page that allows a new user to register
    :return: The response
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_repeat = request.form["password-repeat"]
        recaptcha_result = verify_recaptcha(
            request.remote_addr,
            request.form["g-recaptcha-response"],
            Config().recaptcha_secret_key
        )

        all_users = User.query.all()
        usernames = [user.username for user in all_users]
        emails = [user.email for user in all_users]

        _min, _max = Config.MIN_USERNAME_LENGTH, Config.MAX_USERNAME_LENGTH

        if len(username) < _min or len(username) > _max:
            flash("Username must be betweeen {} and {} characters long"
                  .format(_min, _max), "danger")
        elif ":" in username:
            flash("Username contains illegal character ':'")
        elif password != password_repeat:
            flash("Passwords do not match")
        elif username in usernames:
            flash("Username already exists")
        elif email in emails:
            flash("Email already in use")
        elif not recaptcha_result:
            flash("ReCaptcha not solved correctly")
        else:
            confirmation_key = generate_random(32)
            confirmation_hash = generate_hash(confirmation_key)
            user = User(
                username=username,
                email=email,
                password_hash=generate_hash(password),
                confirmation_hash=confirmation_hash
            )
            db.session.add(user)
            db.session.commit()
            email_msg = render_template(
                "email/registration.html",
                host=request.host,
                target=os.path.join(request.host, "confirm"),
                username=username,
                user_id=user.id,
                confirm_key=confirmation_key
            )
            send_email(
                email,
                "Registration",
                email_msg,
                Config().smtp_host,
                Config().smtp_address,
                Config().smtp_password,
                Config().smtp_port
            )
            flash("Registered Successfully. Check your email inbox for "
                  "confirmation", "info")
            return redirect(url_for("static.index"))
        return redirect(url_for("user_management.register"))
    else:
        return render_template("profile/register.html")


@user_management_blueprint.route("/forgot", methods=["POST", "GET"])
def forgot():
    """
    Allows a user to reset their password
    :return: The response
    """
    if request.method == "POST":
        # TODO
        pass
    else:
        return render_template("profile/forgot.html")
