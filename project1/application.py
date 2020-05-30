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

session={}

@app.route("/")
def index():
    print("session:", session)
    if session.get("user_id") is None:
        return render_template("index.html", log_status=False)
    return render_template("index.html", log_status=True, user_name=session["user"][1])

@app.route("/register")
def register():
    print("session:", session)
    if session.get("user_id") is None:
        return render_template("register.html", log_status=False)
    return render_template("register.html", log_status=True, user_name=session["user"][1])

@app.route("/check_register", methods=["POST"])
def check_register():
    print("session:", session)
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")
    if db.execute("SELECT * FROM accounts WHERE user_name = :user_name", {"user_name": user_name}).rowcount > 0:
        return render_template("error.html", message="There is already user with such a name")
    db.execute("INSERT INTO accounts (user_name, user_pass) VALUES (:user_name, :user_pass)",
            {"user_name": user_name, "user_pass": user_pass})
    db.commit()
    return render_template("success_register.html")
    if session.get("user_id") is None:
        return render_template("success_register.html", log_status=False)
    return render_template("success_register.html", log_status=True, user_name=session["user"][1])

@app.route("/login")
def login():
    print("session:", session)
    if session.get("user_id") is None:
        return render_template("login.html", log_status=False)
    return render_template("login.html", log_status=True, user_name=session["user"][1])


@app.route("/check_login", methods=["GET", "POST"])
def check_login():
    print("session:", session)
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")
    user = db.execute("SELECT id, user_name FROM accounts WHERE user_name = :user_name AND user_pass = :user_pass"
        , {"user_name": user_name, "user_pass": user_pass})
    if user.rowcount == 0:
            return render_template("error.html", message="Invalid user name or password")
    for _ in user:
        session["user_id"] = _[0]
        session["user_name"] =  _[1]
        session["user"] = (_[0], _[1])
    print("session:", session)
    if session.get("user_id") is None:
        return render_template("login.html", log_status=False)
    return render_template("login.html", log_status=True, user_name=session["user"][1])


@app.route("/log-out")
def log_out():
    del session["user_id"]
    del session["user_name"]
    del session["user"]
    return render_template("index.html", log_status=False)

def check_authorization():
    if session.get("user_id") is None:
        print("check_login=> user_id is None!")
        return False, "", ""
    else:
        print("check_login=> user_id is:", session["user_id"])
        print("check_login=> user_name is:", session["user_name"])
        return True, session["user_id"], session["user_name"]

def test_delete():
    user = db.execute("SELECT id, user_name FROM accounts WHERE user_name = 'dima' AND user_pass = 'dima'")
    print("rowcount:", user.rowcount)
    for i in user:
        print("i[0]=", i[0])
        print("i[1]=", i[1])
    #print("session:", session)
#test_delete()
