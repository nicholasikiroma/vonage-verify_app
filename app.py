import os

from dotenv import load_dotenv
from flask import Flask, render_template, abort

from auth.auth import bp as auth_bp
from models import db, User
from post import posts, get_post_by_id

from flask_login import LoginManager, login_required

load_dotenv()

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.register_blueprint(auth_bp)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.login_view = "user_auth.login"

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/content/<int:post_id>")
@login_required
def view_post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        abort(404)
    return render_template("content.html", post=post)


if __name__ == "__main__":
    app.run()
