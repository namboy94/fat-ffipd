import os
from flask import Blueprint, redirect, url_for, request, render_template, flash
from flask_login import login_required, current_user, logout_user, login_user
from puffotter.crypto import generate_hash, generate_random
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
            flash("User already logged in", "info")
        elif not user.confirmed:
            flash("User is not confirmed", "danger")
        elif not user.verify_password(password):
            flash("Invalid Password", "danger")
        else:
            login_user(user, remember=remember_me)
            flash("Logged in successfully", "success")
            app.logger.info("User {} logged in.".format(current_user.username))
            return redirect(url_for("static.index"))
        return redirect(url_for("user_management.login"))
    else:
        return render_template("user_management/login.html")


@user_management_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Logs out the user
    :return: The response
    """
    app.logger.info("User {} logged out.".format(current_user.username))
    logout_user()
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
            flash("Username must be between {} and {} characters long"
                  .format(_min, _max), "danger")
        elif ":" in username:
            flash("Username contains illegal character ':'", "danger")
        elif password != password_repeat:
            flash("Passwords do not match", "danger")
        elif username in usernames:
            flash("Username already exists", "danger")
        elif email in emails:
            flash("Email already in use", "danger")
        elif not recaptcha_result:
            flash("ReCaptcha not solved correctly", "danger")
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
            app.logger.info("User {} registered.".format(user.username))
            flash("Registered Successfully. Check your email inbox for "
                  "confirmation", "info")
            return redirect(url_for("static.index"))
        return redirect(url_for("user_management.register"))
    else:
        return render_template("user_management/register.html")


@user_management_blueprint.route("/confirm", methods=["GET"])
def confirm():
    """
    Confirms a user
    :return: The response
    """
    user_id = int(request.args["user_id"])
    confirm_key = request.args["confirm_key"]
    existing = {user.id: user for user in User.query.all()}
    user: User = existing.get(user_id)

    if user is None:
        flash("User does not exist", "danger")
    elif user.confirmed:
        flash("User already confirmed", "warning")
    elif not user.verify_confirmation(confirm_key):
        flash("Confirmation key invalid", "warning")
    else:
        print("D")
        user.confirmed = True
        db.session.commit()
        flash("User confirmed successfully", "success")
    return redirect(url_for("static.index"))


@user_management_blueprint.route("/forgot", methods=["POST", "GET"])
def forgot():
    """
    Allows a user to reset their password
    :return: The response
    """
    if request.method == "POST":
        email = request.form["email"]
        recaptcha_result = verify_recaptcha(
            request.remote_addr,
            request.form["g-recaptcha-response"],
            Config().recaptcha_secret_key
        )
        existing = {user.email: user for user in User.query.all()}
        user: User = existing.get(email)

        if not recaptcha_result:
            flash("Invalid ReCaptcha Response", "danger")
            return redirect(url_for("user_management.forgot"))
        else:
            if user is None:
                # Fail silently to ensure that a potential attacker can't use
                # the response to figure out information on registered users
                pass
            else:
                new_pass = generate_random(20)
                user.password_hash = generate_hash(new_pass)
                db.session.commit()

                email_msg = render_template(
                    "email/forgot_password_email.html",
                    host=request.host,
                    target=os.path.join(request.host, "login"),
                    password=new_pass,
                    username=user.username
                )
                send_email(
                    email,
                    "Password Reset",
                    email_msg,
                    Config().smtp_host,
                    Config().smtp_address,
                    Config().smtp_password,
                    Config().smtp_port
                )
            flash("Password was reset successfully", "success")
            return redirect(url_for("static.index"))

    else:
        return render_template("user_management/forgot.html")


@user_management_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    """
    Allows a user to edit their profile details
    :return: The response
    """
    return render_template("user_management/profile.html")


@user_management_blueprint.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """
    Allows the user to change their password
    :return: The response
    """
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]
    password_repeat = request.form["password_repeat"]
    user: User = current_user

    if new_password != password_repeat:
        flash("Passwords do not match", "danger")
    elif not user.verify_password(old_password):
        flash("Invalid Password", "danger")
    else:
        user.password_hash = generate_hash(new_password)
        db.session.commit()
        flash("Password changed successfully", "success")
    return redirect(url_for("user_management.profile"))


@user_management_blueprint.route("/delete_user", methods=["POST"])
@login_required
def delete_user():
    """
    Allows a user to delete their account
    :return: The response
    """
    password = request.form["password"]
    user: User = current_user

    if not user.verify_password(password):
        flash("Invalid Password", "danger")
    else:
        app.logger.info("Deleting user {}".format(user))
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash("User was deleted", "success")
        return redirect(url_for("static.index"))
    return redirect(url_for("user_management.profile"))
