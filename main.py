from flask import Flask, render_template, request, session, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os.path import join, dirname, realpath
import re

app = Flask(__name__)

app.secret_key = "altinss2223442"

# database

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foto2.db"

db = SQLAlchemy(app)

# session

# bcrypt

bcrypt = Bcrypt(app)

# upload

UPLOAD_FOLDER = join(dirname(realpath(__file__)))
ALLOWED_EXTENSIONS = ["png", "jpeg", "gif", "jpeg"]

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<Title : %s>" % self.email

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

    def __repr__(self):
        return "<Title : %s>" % self.email

class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    album_id = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<Title : %s>" % self.email


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/dashboard", methods=['POST', 'GET'])

def dashboard():
    if session['is_logged_in'] != True:
        return """
        <p>
            You are not allowed to visit this site without authorization
        <p>
        <a href="/login">Log in</a>
        """
    return render_template("admin/dashboard.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if not_empty([username, email, password, confirm_password]):
            if is_email(email):
                if passwords_match(password, confirm_password):
                    password_hash = bcrypt.generate_password_hash(password)
                    user = User(username, email, password_hash)
                    db.session.add(user)
                    db.session.commit()
                    # create session items ( we will need these in dashboard,album and photos )
                    session["is_logged_in"] = True
                    session["email"] = email
                    session["username"] = username
                    return redirect(url_for("dashboard"))
                else:
                    flash("passwords do not match")
            else:
                flash("try another email")
        else:
            flash("all fields should be filled.")
        return redirect(url_for("register"))

    return render_template("auth/register.html")

@app.route("/login", methods=['POST', 'GET'])

def login():
    session['username'] = ""
    session['email'] = ""
    session['is_logged_in'] = False
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if not_empty([email, password]):
            if is_email(email):
                user = User.query.filter_by(email=email).first()
                if user:
                    if bcrypt.check_password_hash(user.password, password):
                        session["is_logged_in"] = True
                        session["username"] = user.username
                        session["email"] = email
                        return redirect(url_for("dashboard"))
                    else:
                        flash("Incorrect password")
                else:
                    flash("Unknown Username")
            else:
                flash("try another email")
        else:
            flash("all fields are required")
        return redirect(url_for("login"))
    else:
        if session["is_logged_in"]:
            return redirect(url_for("dashboard"))
        return render_template("auth/login.html")

@app.route("/logout")
def logout():
    session['username'] = ""
    session['email'] = ""
    session['is_logged_in'] = False
    return render_template("home.html")


def not_empty(form_fields):
    for field in form_fields:
        if len(field) == 0:
            return False
    return True



def is_email(email):
    return re.search("[\w\.\_\-]+\@[\w\-]+\.[a-z]{2,5}", email)

def passwords_match(password, confirm_password):
    return password == confirm_password



@app.route("/albums", methods=['GET','POST'])
def albums():
    return None

@app.route("/photos/<int:album_id>", methods=["POST", "GET"])
def photos():
    return None



if __name__ == "__main__":
    app.run(debug=True)