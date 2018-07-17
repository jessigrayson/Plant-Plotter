"""Garden Plants."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Plant, User, UserGarden, Water, Sun, ZipFrostDate, UserPlanted

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# It raises an error if you use an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Homepage."""
    plants = Plant.query.all()

    return render_template("homepage.html", plants=plants)


# @app.route('/', methods=['POST'])
# def process_plant_request():
#     """Homepage plant info request."""


#     return render_template("plant.html", plant_id=plant.plant_id)


@app.route("/plant/<int:plant_id>", methods=['GET'])
def plant_detail(plant_id):
    """Show plant and associated info."""

    # plant = db.session.query(Plant).filter_by(pname=pname).first()

    return render_template("plant.html", plant_id=plant_id)


# @app.route('/', methods=['POST'])
# def index():
#     """Homepage."""

#     testplant = Strawberry
#     # see if plant is in db and get id
#     # if in db, then render template to /plant
#     # if not in db, then alert or something saying not in our db
#     # if plant:
#     #     #get the plant object from db
#     # else:
#     #     plant = None
#     # return render_template("plant.html", testplant=testplant)
#     return render_template("plant.html", plant_id=testplant)


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("user_reg.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    reg_date = datetime.date

    new_user = User(fname=fname,
                    lname=lname,
                    email=email,
                    zipcode=zipcode,
                    username=username,
                    password=password,
                    reg_date=reg_date)

    db.session.add(new_user)
    db.session.commit()

    flash("User {username} added.")
    return redirect("/users/{new_user.user_id}")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = db.session.filter(user_id).first()

    return render_template("user.html", user=user)


@app.route("/garden/<int:user_id>")
def garden_detail(user_id):
    """Show user garden(s) & associated info."""

    user = session.get("user_id")

    garden = db.session.query.options(garden_id)

    return render_template("user_garden.html, user=user")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
