"""Garden Plants."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
# from flask_login import login_required, current_user (Phase 2?)
from datetime import datetime

from model import connect_to_db, db, Plant, User, UserGarden, Water, Sun, GardenPlants
#ZipFrostDate

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Homepage."""

    plants = Plant.query.all()
    # plants = db.session.query(Plant).order_by('pname').all()

    return render_template("homepage.html", plants=plants)


@app.route("/plant", methods=['GET'])
def plant_detail():
    """Show plant and associated info."""

    plant_id = int(request.args.get("plants"))
    plant = Plant.query.get(plant_id)

    return render_template("plant.html", plant=plant)


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("new_user.html")


@app.route('/register', methods=['POST'])
def process_registration():
    """Process registration."""

    if session:
        flash("You are already logged in.")
        return redirect("/")

    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    zipcode = request.form["zipcode"]

    reg_date = datetime.now()

    new_user = User(fname=fname,
                    lname=lname,
                    email=email,
                    zipcode=zipcode,
                    username=username,
                    password=password,
                    reg_date=reg_date)

    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.user_id

    flash("User {} added".format(username))
    return redirect("/user")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def process_login():
    """Process login."""

    username = request.form["username"]
    print(username)
    password = request.form["password"]
    print(password)

    user = User.query.filter(User.username == username).first()
    # CHANGE TO .ONE() AND MAKE AN ERROR EXCEPTION

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    return redirect("/mygarden")


@app.route('/logout')
def logout():
    """Log out."""

    if session:
        del session["user_id"]

    flash("Logged Out.")

    return redirect("/")


@app.route("/user")
def user_detail():
    """Show info about user."""

    if not session:
        flash("You have not yet logged in.")

        return redirect("/login")

    user = User.query.get(session['user_id'])

    return render_template("user.html", user=user)


@app.route("/mygarden")
# @login_required
def garden_detail():
    """Show user garden(s) & associated info."""
    if not session:
        flash("You need to login to view your garden")
        return redirect("/")

    user = User.query.get(session["user_id"])

    usergardens = user.usergarden

    return render_template("garden.html",
                           user=user,
                           usergardens=usergardens)


@app.route("/addgarden", methods=['GET', 'POST'])
def add_garden():
    if not session:
        flash("You must be logged in to create a garden")
        return redirect("/login")
    user = User.query.get(session["user_id"])

    usergardens = user.usergarden

    sun_exposures = Sun.query.all()

    if request.method == 'POST':
        if not request.form["sun"] or not request.form["garden_name"] or not request.form["garden_desc"]:

            flash("Please enter all the fields", "error")
        else:
            garden_name = request.form["garden_name"]
            garden_desc = request.form["garden_desc"]
            sun_id = request.form["sun"]

            new_usergarden_obj = UserGarden(user_id=user.user_id,
                                            garden_name=garden_name,
                                            garden_desc=garden_desc,
                                            sun_id=sun_id)

            db.session.add(new_usergarden_obj)
            db.session.commit()

            flash("{} successfully added as a garden".format(garden_name))
            return redirect("/addplant")

    return render_template("add_garden.html", user=user, usergardens=usergardens, sun_exposures=sun_exposures)


@app.route("/addplant", methods=['GET', 'POST'])
def add_plant():
    """Select a plant to add to one of your gardens"""

    if not session:
        flash("You must be logged in to add plants")
        return redirect("/login")

    user = User.query.get(session["user_id"])

    usergardens = user.usergarden

    plants = Plant.query.all()

    if request.method == 'POST':
        if not request.form["plant"] or not request.form["planted_date"] or not request.form["garden"]:

            flash("Please enter all the fields", "error")

        else:
            usergarden_id = request.form["garden"]
            usergarden = UserGarden.query.get(usergarden_id)

            plant_id = request.form["plant"]
            plant_obj = Plant.query.get(plant_id)

            planted_date_str = request.form["planted_date"]
            dt_planted_date = datetime.strptime(planted_date_str, '%Y-%m-%d')
            planted_date = dt_planted_date.date()

            harvest_date = GardenPlants.calculate_harvest_date(plant_obj.plant_id, planted_date)

            new_gardenplant_obj = GardenPlants(garden_id=usergarden.garden_id,
                                               plant_id=plant_obj.plant_id,
                                               planted_date=planted_date,
                                               harvest_date=harvest_date)

            db.session.add(new_gardenplant_obj)
            db.session.commit()

            flash("{} successfully added to {}".format(plant_obj.pname, usergarden.garden_name))
            return redirect("/mygarden")

    return render_template("add_plant.html", user=user, usergardens=usergardens, plants=plants)


@app.route("/editgarden", methods=['GET', 'POST'])
def edit_garden():
    """add, remove, or change gardens and/or plant information in db"""

    return render_template("editgarden.html")

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
