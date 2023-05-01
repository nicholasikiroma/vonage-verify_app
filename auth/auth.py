from flask import Blueprint, render_template
from models import LoginForm, SignupForm, TwoFactorForm

bp = Blueprint("user_auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@bp.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)

@bp.route("/validate", methods=["POST", "GET"])
def validate():
    form = TwoFactorForm()
    return render_template("validate.html", form=form)

@bp.route("/logout")
def logout():
    pass
