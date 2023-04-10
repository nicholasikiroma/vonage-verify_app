from flask import Blueprint, render_template

bp = Blueprint("user_auth", __name__, url_prefix="/auth")


@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/signup")
def signup():
    return render_template("signup.html")

@bp.route("/validate")
def validate():
    return render_template("validate.html")

@bp.route("/logout")
def logout():
    pass