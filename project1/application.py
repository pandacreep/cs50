import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/check_register", methods=["POST"])
def check_register():
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")
    if db.execute("SELECT * FROM accounts WHERE user_name = :user_name", {"user_name": user_name}).rowcount > 0:
        return render_template("error.html", message="There is already user with such a name")
    db.execute("INSERT INTO accounts (user_name, user_pass) VALUES (:user_name, :user_pass)",
            {"user_name": user_name, "user_pass": user_pass})
    db.commit()
    return render_template("success_register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/check_login", methods=["POST"])
def check_login():
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")
    if db.execute("SELECT * FROM accounts WHERE user_name = :user_name AND user_pass = :user_pass", {"user_name": user_name, "user_pass": user_pass}).rowcount == 0:
            return render_template("error.html", message="Invalid user name or password")
    return render_template("success_login.html")
