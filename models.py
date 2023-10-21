from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TelField, StringField, PasswordField
from wtforms.validators import InputRequired, equal_to
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """Table for storing registered users"""

    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    phone_no = db.Column(db.Integer(), nullable=False)
    password = db.Column(db.String(), nullable=False)


class SignupForm(FlaskForm):
    """Validations for signup form"""

    username = StringField(
        label="Username", validators=[InputRequired(message="Provide a username")]
    )
    phone_no = TelField(
        label="Phone Number",
        validators=[InputRequired(message="Provide a valid phone number")],
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired(message="Password cannot be left blank")],
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[
            InputRequired(message="Password cannot be left blank"),
            equal_to("password", message="passwords do not match"),
        ],
    )


class LoginForm(FlaskForm):
    """Validation for login form"""

    username = StringField(
        label="Username", validators=[InputRequired(message="Provide a username")]
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired(message="Password cannot be left blank")],
    )


class TwoFactorForm(FlaskForm):
    """Validation for two-factor form"""

    code = StringField(
        label="Enter Code:", validators=[InputRequired(message="Enter valid code")]
    )
