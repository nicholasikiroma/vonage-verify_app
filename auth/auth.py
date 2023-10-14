import os
import vonage

from dotenv import load_dotenv

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import LoginForm, SignupForm, TwoFactorForm
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, db

bp = Blueprint("user_auth", __name__, url_prefix="/auth")


load_dotenv()

client = vonage.Client(key=os.getenv("VONAGE_KEY"), secret=os.getenv("VONAGE_SECRET"))
verify = vonage.Verify2(client)


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            phone_no = str(user.phone_no)

            try:
                response = verify.new_request(
                    {
                        "brand": "Vonage Verify",
                        "workflow": [{"channel": "sms", "to": "234" + phone_no}],
                    }
                )

                return redirect(
                    url_for(
                        "user_auth.validate",
                        user_id=user.id,
                        res_id=response["request_id"],
                    )
                )
            except vonage.Verify2Error as err:
                print(str(err))
                flash("Failed to verify")
                return render_template("login.html", form=form)

        else:
            flash("Username/password incorrect")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@bp.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()

    if request.method == "POST" and form.validate_on_submit():
        username = request.form.get("username")
        phone_no = request.form.get("phone_no")
        password = request.form.get("password")

        # hash password
        password_hash = generate_password_hash(password)

        # Create a new user instance
        new_user = User(username=username, phone_no=phone_no, password=password_hash)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!")
            return redirect(url_for("user_auth.login"))

        except IntegrityError:
            flash("User with username already exists")
            return render_template("signup.html", form=form)

        except SQLAlchemyError:
            flash(
                "An unknown error occured.\
                  Please try again later."
            )
            return render_template("signup.html", form=form)

    return render_template("signup.html", form=form)


@bp.route("/validate/user/<int:user_id>/<string:res_id>", methods=["POST", "GET"])
def validate(user_id, res_id):
    form = TwoFactorForm()

    if request.method == "POST" and form.validate_on_submit():
        passcode = int(request.form.get("code"))
        user = User.query.filter_by(id=user_id).first()

        try:
            response = verify.check_code(res_id, passcode)
            login_user(user)
            return redirect(url_for("index"))

        except vonage.Verify2Error as err:
            flash(str(err))

    return render_template("validate.html", form=form, user_id=user_id, res_id=res_id)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
