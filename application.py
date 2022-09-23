import os

from flask import Flask, render_template, session, request, redirect, url_for, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# configuring session to use filesystem

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for('search'))
    return render_template("index.html")

@app.route("/search1",methods=["GET"])
def search1():
    if "username" in session:
        session.pop("username")
    return redirect(url_for('search'))

@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "GET":
        if "username" in session:
            return render_template("search.html",loggedIn=1)
        return render_template("search.html",loggedIn=0)
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if (username is None) or (password is None):
            return render_template("error.html",message="Username and Password should not be blank")

        if "name" in request.form:
            usersWithSelectedUsername = db.execute("select * from users where username=:username",{"username":username}).fetchall()
            if len(usersWithSelectedUsername) != 0:
                return render_template("error.html",message="Username already exists")
            name = request.form.get("name")
            age = request.form.get("age")
            phone = request.form.get("phone")

            if name is None:
                return render_template("error.html",message="Name should not be blank")
            if age is None:
                return render_template("error.html",message="Age should not be blank")
            if phone is None:
                return render_template("error.html",message="Phone number should not be blank")        

            db.execute("insert into users (name,age,phone,username,password) values (:name,:age,:phone,:username,:password)",{"name":name,"age":age,"phone":phone,"username":username,"password":password}) 
            db.commit()   
            session["username"] = username
        else:
            user = db.execute("select * from users where username=:username and password=:password",{"username":username,"password":password}).fetchall()
            if len(user) == 0:
                return render_template("error.html",message="wrong username or password")
            session["username"] = username
    return render_template("search.html",loggedIn=1)


@app.route("/books",methods=["POST"])
def books():
    print("yes")
    titleChars=request.form.get("title")
    isbnChars=request.form.get("isbn")
    authorChars=request.form.get("author")
    allTitles=db.execute("SELECT title FROM books WHERE author iLIKE '%"+authorChars+"%' and title iLIKE '%"+titleChars+"%' and isbn iLIKE '%"+isbnChars+"%'").fetchall()
    allISBNs=db.execute("SELECT isbn FROM books WHERE author iLIKE '%"+authorChars+"%' and title iLIKE '%"+titleChars+"%' and isbn iLIKE '%"+isbnChars+"%'").fetchall()

    d = {}
    for j in range(0,len(allTitles)):
        isbn=allISBNs[j][0]
        title=allTitles[j][0]
        d[isbn]=title

    return jsonify(d)


@app.route("/book/<string:isbn>",methods=["GET","POST"])
def book(isbn):
    if request.method == "POST":
        username = session["username"]
        userRating = request.form.get("rating")
        userReview = request.form.get("review")
        book = db.execute("select * from books where isbn=:isbn",{"isbn":isbn}).fetchone()
        avgRating = db.execute("select avg(rating) from reviews where isbn=:isbn",{"isbn":isbn}).fetchone()
        reviews = db.execute("select * from reviews where isbn=:isbn",{"isbn":isbn}).fetchall()
        if avgRating[0] is not None:
            avgRating=float(avgRating[0])        
        if db.execute("select * from reviews where username=:username and isbn=:isbn",{"username":username,"isbn":isbn}).fetchone() is not None:
            return render_template("book2.html",book=book,rating=avgRating,reviews=reviews)
        db.execute("insert into reviews (username,isbn,rating,review) values (:username,:isbn,:rating,:review)",{"username":username, "isbn":isbn, "rating":userRating, "review":userReview})
        db.commit() 

    book = db.execute("select * from books where isbn=:isbn",{"isbn":isbn}).fetchone()
    avgRating = db.execute("select avg(rating) from reviews where isbn=:isbn",{"isbn":isbn}).fetchone()
    reviews = db.execute("select * from reviews where isbn=:isbn",{"isbn":isbn}).fetchall()

    if avgRating[0] is not None:
        avgRating = float(avgRating[0])

    if "username" not in session:
        return render_template("book1.html",book=book,rating=avgRating,reviews=reviews)
    username = session["username"]
    if db.execute("select * from reviews where username=:username and isbn=:isbn",{"username":username,"isbn":isbn}).fetchone() is not None:
        return render_template("book2.html",book=book,rating=avgRating,reviews=reviews)
    
    return render_template("book.html",book=book,rating=avgRating,reviews=reviews)
    

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for('index')) 

@app.route("/api/<string:isbn>")
def api(isbn):
    book=db.execute("select * from books where isbn=:isbn",{"isbn":isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid"}), 404    
    numOfReviews=db.execute("select count(rating) from reviews where isbn=:isbn",{"isbn":isbn}).fetchone()
    if numOfReviews[0] is not None:
        numOfReviews = int(numOfReviews[0]) 
    else:
        numOfReviews = 0
    avgRating=db.execute("select avg(rating) from reviews where isbn=:isbn",{"isbn":isbn}).fetchone()
    if avgRating[0] is not None:
        avgRating = float(avgRating[0])
    return jsonify({
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "number of reviews": numOfReviews,
        "average rating": avgRating
    })     

if __name__ == "__main__":
    app.run(debug=True)          
