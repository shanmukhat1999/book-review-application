import os

from flask import Flask, render_template, session, request, redirect, url_for, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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


@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "GET":
        if "username" in session:
            return render_template("search.html",t=1)
        return render_template("search.html",t=0)      
    else:
        username=request.form.get("username")
        password=request.form.get("password")
        if "name" in request.form:
            k=db.execute("select * from users where username=:username",{"username":username}).fetchall()
            name=request.form.get("name")
            age=request.form.get("age")
            phone=request.form.get("phone")
            if len(k) != 0:
                return render_template("error.html",message="choose another username")
            db.execute("insert into users (name,age,phone,username,password) values (:name,:age,:phone,:username,:password)",{"name":name,"age":age,"phone":phone,"username":username,"password":password}) 
            db.commit()   
            session["username"]=username
        else:
            p=db.execute("select * from users where username=:username and password=:password",{"username":username,"password":password}).fetchall()
            if len(p) == 0:
                return render_template("error.html",message="wrong username or password")
            session["username"]=username 
    return render_template("search.html",t=1)   


@app.route("/books",methods=["POST"])
def books():
    print("yes")
    title=request.form.get("title")
    isbn=request.form.get("isbn")
    author=request.form.get("author")
    t=db.execute("SELECT title FROM books WHERE author iLIKE '%"+author+"%' and title iLIKE '%"+title+"%' and isbn iLIKE '%"+isbn+"%'").fetchall()
    i=db.execute("SELECT isbn FROM books WHERE author iLIKE '%"+author+"%' and title iLIKE '%"+title+"%' and isbn iLIKE '%"+isbn+"%'").fetchall()

    d = {}
    for j in range(0,len(t)):
        r=i[j][0]
        s=t[j][0]
        d[r]=s
    return jsonify(d)   


@app.route("/book/<string:isbn>",methods=["GET","POST"])
def book(isbn):
    if request.method == "POST":
        username=session["username"]
        rate=request.form.get("rating")
        review=request.form.get("review")
        k=db.execute("select * from books where isbn=:isbn",{"isbn":isbn}).fetchone()
        rating=db.execute("select avg(rating) from reviews where isbn=:isbn",{"isbn":isbn}).fetchone()
        r=db.execute("select * from reviews where isbn=:isbn",{"isbn":isbn}).fetchall()
        q=rating[0]
        if q is not None:
            q=float(q)
        s=db.execute("select * from reviews where username=:username and isbn=:isbn",{"username":username,"isbn":isbn}).fetchone()        
        if s is not None:
            return render_template("book2.html",book=k,rating=q,r=r)
        db.execute("insert into reviews (username,isbn,rating,review) values (:username,:isbn,:rating,:review)",{"username":username,"isbn":isbn,"rating":rate,"review":review})
        db.commit() 

    k=db.execute("select * from books where isbn=:isbn",{"isbn":isbn}).fetchone()
    rating=db.execute("select avg(rating) from reviews where isbn=:isbn",{"isbn":isbn}).fetchone()
    r=db.execute("select * from reviews where isbn=:isbn",{"isbn":isbn}).fetchall()

    q=rating[0]
    if q is not None:
        q=float(q)

    if "username" not in session:
        return render_template("book1.html",book=k,rating=q,r=r)
    username=session["username"] 
    s=db.execute("select * from reviews where username=:username and isbn=:isbn",{"username":username,"isbn":isbn}).fetchone()        
    if s is not None:
        return render_template("book2.html",book=k,rating=q,r=r)
    
    return render_template("book.html",book=k,rating=q,r=r)    
    

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for('index')) 

@app.route("/api/<string:isbn>")
def api(isbn):
    n=db.execute("select * from books where isbn=:isbn",{"isbn":isbn}).fetchone()
    if n is None:
        return jsonify({"error": "Invalid"}), 404    
    count=db.execute("select count(rating) from reviews where isbn=:isbn",{"isbn":isbn}).fetchone()
    count=count[0]
    if count is not None:
        count=int(count) 
    else:
        count=0    
    s=db.execute("select avg(rating) from reviews where isbn=:isbn",{"isbn":isbn}).fetchone()
    q=s[0]
    if q is not None:
        q=float(q)
    return jsonify({
        "isbn":n.isbn,
        "title":n.title,
        "author":n.author,
        "year":n.year,
        "review count":count,
        "average rating":q
    })     

if __name__ == "__main__":
    app.run(debug=True)             



                


