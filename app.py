import os

from dotenv import load_dotenv
from flask import Flask, render_template
# from flask_login import LoginManager


from auth.auth import bp as auth_bp
from models import db, User

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.register_blueprint(auth_bp)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
