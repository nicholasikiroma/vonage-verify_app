from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, SignupForm, LoginForm, db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

bp = Blueprint("user_auth", __name__, url_prefix="/auth")


@bp.route("/login")
def login():
    pass


@bp.route("/signup", methods=["POST", "GET"])
def signup():
    pass

@bp.route("/validate")
def validate():
    return render_template("validate.html")

@bp.route("/logout")
def logout():
    pass