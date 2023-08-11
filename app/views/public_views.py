from flask import Blueprint, render_template, request, redirect, flash, g, url_for, session
from ..database.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from peewee import DoesNotExist, OperationalError, DatabaseError
import functools
bp = Blueprint("home", __name__)


@bp.before_app_request
def load_logged_in_user():
    username = session.get("username")

    if username is None:
        g.user = None
    else:
        try:
            g.user = User.get(User.username == username)

        except OperationalError:
            print("You should have initialized the database.")
        except DoesNotExist:
            session.clear()
            print("A previous session was active, cleared it now!")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('home.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route("/")
def index():
    return render_template("public/index.html")


@bp.route("/about")
def about():
    return render_template("public/about.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        try:
            user = User.get(User.username == username)
        except DoesNotExist:
            error = f"User {username} does not exist."
        else:
            if not check_password_hash(user.password, password):
                error = "Incorrect password."

        if error is None:
            session.clear()
            session["username"] = user.username
            return redirect(url_for("home.index"))

        flash(error)

    return render_template("public/login.html")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]
        billing = request.form["billing"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                item = User(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    address_data=address,
                    billing_information=billing
                )
                item.save()
            except DatabaseError as e:
                # error = f"User {username} is already registered."
                error = e
            else:
                return redirect(url_for("home.login"))

        flash(error)

    return render_template("public/register.html")


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
