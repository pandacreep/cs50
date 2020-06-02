import os, requests

from flask import Flask, session, render_template, request, jsonify
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

# Initialize variables
session={}

@app.route("/")
def index():
    return render_template("index.html", user_name=user_authorized())


@app.route("/register")
def register():
    return render_template("register.html", user_name=user_authorized())


@app.route("/check_register", methods=["POST"])
def check_register():
    print("session:", session)
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")
    if db.execute("SELECT * FROM accounts WHERE user_name = :user_name", {"user_name": user_name}).rowcount > 0:
        return render_template("error.html", user_name=user_authorized(), message="There is already user with such a name")
    db.execute("INSERT INTO accounts (user_name, user_pass) VALUES (:user_name, :user_pass)",
            {"user_name": user_name, "user_pass": user_pass})
    db.commit()
    return render_template("success_register.html", user_name=user_authorized())


@app.route("/login")
def login():
    return render_template("login.html", user_name=user_authorized())


@app.route("/check_login", methods=["GET", "POST"])
def check_login():
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")
    user = db.execute("SELECT id, user_name FROM accounts WHERE user_name = :user_name AND user_pass = :user_pass"
        , {"user_name": user_name, "user_pass": user_pass})
    if user.rowcount == 0:
            return render_template("error.html", user_name=user_authorized(), message="Invalid user name or password")
    for _ in user:
        session["user_id"] = (_[0], _[1])
    return render_template("index.html", user_name=user_authorized())


@app.route("/log-out")
def log_out():
    del session["user_id"]
    return render_template("index.html", user_name=user_authorized())


@app.route("/books", methods=["POST"])
def books():
    if user_authorized() == "":
        return render_template("error.html", user_name=user_authorized(), message="Please login before making any search")
    search_string = request.form.get("search_string")
    search_string = '%' + search_string +'%'
    sql_script = """
    SELECT * FROM books
    WHERE title like :search_string
    OR author like :search_string
    OR isbh like :search_string
    """
    search_result = db.execute(sql_script, {"search_string": search_string})
    if search_result.rowcount == 0:
        return render_template("books.html", user_name=user_authorized(), message="No results are found", search_result=search_result)
    return render_template("books.html",
                            user_name=user_authorized(),
                            search_result=search_result)

@app.route("/books/<string:book_isbh>")
def book(book_isbh):
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbh = :isbh", {"isbh": book_isbh}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book")

    # Get all reviews information
    sql_script = """
    SELECT r.user_id, a.user_name, r.rate_score, r.rate_text
    FROM reviews r
    JOIN accounts a ON r.user_id = a.id
    WHERE r.isbh = :isbh
    """
    reviews = db.execute(sql_script, {"isbh": book_isbh}).fetchall()
    session["isbn"] = book_isbh

    try:
        key = "m4Op1odc9VVDWVL0UOC9A"
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": book_isbh})
        #print("book_isbh:", book_isbh)
        #sprint("res:", res)
        goodreads_rate = res.json()['books'][0]['average_rating']
        goodreads_count = res.json()['books'][0]['work_reviews_count']
        goodreads_result = "This book has " +  str(goodreads_rate) + " rate from " + str(goodreads_count) + " reviews on Goodreads.com website"
    except:
        goodreads_result = "Some errors occur during connections to Goodreads.com website"
    print(goodreads_result)
    return render_template("book.html",
                            book=book,
                            reviews=reviews,
                            goodreads_result=goodreads_result,
                            user_name=user_authorized())


@app.route("/api//books/<string:book_isbh>")
def book_api(book_isbh):
    # Make sure book exists
    book = db.execute("SELECT * FROM books WHERE isbh = :isbh", {"isbh": book_isbh}).fetchone()
    if book is None:
        return jsonify({"error": "404"}), 404
    sql_script = """
    SELECT count(isbh) count, avg(rate_score) avg
    FROM reviews
    WHERE isbh = :isbh
    GROUP BY isbh
    """
    reviews = db.execute(sql_script, {"isbh": book_isbh}).fetchone()

    # Make sure reviews exist
    if reviews is None:
        reviews = (0, 0)
    print("reviews:", reviews)
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbh,
        "review_count": str(reviews[0]),
        "average_score": str(reviews[1])
        })
    print('book_api=> ending')


@app.route("/add_review", methods=["POST"])
def add_review():
    rate_score = request.form.get("review_score")
    rate_text = request.form.get("review_text")
    check_review = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND isbh = :isbh"
        , {"user_id": session["user_id"][0], "isbh": session["isbn"]})
    if check_review.rowcount > 0:
        return render_template("error.html", message="You already posted review on this book", user_name=user_authorized())
    db.execute("INSERT INTO reviews (user_id, isbh, rate_score, rate_text) VALUES (:user_id, :isbh, :rate_score, :rate_text)",
            {"user_id": session["user_id"][0], "isbh": session["isbn"], "rate_score": rate_score, "rate_text": rate_text})
    db.commit()
    return render_template("success_add_review.html", user_name=user_authorized())


# Check you anybody is logged in. Return user name. If nobody is logged in return empty string
def user_authorized():
    #print("user_authorized=> session:", session)
    if session.get("user_id") is None:
        user_name = ""
    else:
        user_name = session["user_id"][1]
    return user_name
