import os
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
    session,
)
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests
import os
from colorthief import ColorThief
from robohash import Robohash


def CreateProfilePicture(hash):
    path = "pictures/"
    rh = Robohash(hash)
    rh.assemble(roboset="set1")
    with open(path + hash + "ProfilePicture" + ".png", "wb") as f:
        rh.img.save(f, format="png")

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MYSQL_HOST"] = "146.59.33.189"
app.config["MYSQL_USER"] = "rps"
app.config["MYSQL_PASSWORD"] = "Fit&Fun13"
app.config["MYSQL_DB"] = "rps"
mysql = MySQL(app)


API_USER = "RPS-USER"
# API_URL = "http://146.59.33.189:3000"
API_URL = "http://127.0.0.1:3000"


class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=4, max=50)],
        render_kw={"placeholder": "email"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "password"},
    )
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=4, max=50)],
        render_kw={"placeholder": "email"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "password"},
    )
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=30)],
        render_kw={"placeholder": "username"},
    )
    submit = SubmitField("Register")


@app.route("/")
def index():
    return "Hello"


@app.route("/login", methods=["GET", "POST"])
def login():
    login_from = LoginForm()
    if (
        request.method == "POST"
        and "email" in request.form
        and "password" in request.form
    ):
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM users WHERE Email = %s AND Password = %s",
            (
                email,
                password,
            ),
        )
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session["isloggedin"] = True
            session["id"] = account["UserID"]
            session["username"] = account["Username"]
            # Redirect to home page
            return redirect(url_for("lobbies"))
        else:
            flash("incorrect username or password.")
    return render_template("login.html", form=login_from)


@app.route("/register", methods=["GET", "POST"])
def register():
    register = RegisterForm()
    if (
        request.method == "POST"
        and "email" in request.form
        and "password" in request.form
        and "username" in request.form
    ):
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        response = requests.post(
            API_URL + "/CreateNewUser",
            params={
                "email": email,
                "password": password,
                "username": username,
                "ApiUser": API_USER,
            },
        )
        if response.status_code == 200:
            print(response.json())
            session["id"] = response.json()["UserID"]
            session["username"] = response.json()["username"]
            session["isloggedin"] = True
            CreateProfilePicture(str(session["username"]))
            return redirect(url_for("lobbies"))
        else:
            return "Wrong register dataa"
    return render_template("register.html", form=register)


@app.route("/lobbies", methods=["GET", "POST"])
def lobbies():
    if "username" in session:
        coins = requests.get(API_URL + "/GetUserBalance/" + str(session["id"])).json()[
            "balance"
        ]
        ProfilePicture = "https://robohash.org/" + str(session["username"])
        
        color_thief = ColorThief(f"pictures/{str(session['username'])}ProfilePicture.png")
        color = color_thief.get_color(quality=1)
        return render_template(
            "lobbies.html", coins=coins, ProfilePicture=ProfilePicture, color=color
        )
    else:
        return redirect(url_for("login"))


@app.route("/history", methods=["GET", "POST"])
def history():
    if "username" in session:
        coins = requests.get(API_URL + "/GetUserBalance/" + str(session["id"])).json()[
            "balance"
        ]
        ProfilePicture = "https://robohash.org/" + str(session["username"])
        CreateProfilePicture(str(session["username"]))
        color_thief = ColorThief(f"pictures/{str(session['username'])}ProfilePicture.png")
        color = color_thief.get_color(quality=1)
        return render_template(
            "history.html", coins=coins, ProfilePicture=ProfilePicture, color=color
        )
    else:
        return redirect(url_for("login"))


@app.route("/spin")
def spin():
    return "spin"

@app.route("/account")
def account():
    return "account"

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon/favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run(port=80)
