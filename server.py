"""Garden Plants."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
# from flask_login import login_required, current_user (Phase 2?)

from model import connect_to_db, db, Plant, User, UserGarden, Water, Sun, ZipFrostDate, UserPlanted

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

    return render_template("user_reg.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    reg_date = datetime.datetime.now()

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
    # Needs action for when nav bar pulls this route
    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = db.session.filter(user_id).get()

    return render_template("user.html", user=user)


@app.route("/mygarden")
# @login_required
def garden_detail():
    """Show user garden(s) & associated info."""

    user = User.query.get(session["user_id"])

    usergardens = user.usergarden

    # gardenplants = user.gardenplants
    gardenplants = garden.gardenplants

    return render_template("garden.html",
                           user=user,
                           usergardens=usergardens,
                           gardenplants=gardenplants)


@app.route("/addgarden", methods='GET', 'POST')
def add_garden():
    # page will show form to add a garden with all the parameters
    # upon submitting form, a new garden object will be instantiated
    # then that info will pass to the add plants page
    # would like to (eventually) add plants which will be in AJAX/JS
    # so one can stay on the page and continually add plants.
    #     plant_id = int(request.args.get("plants"))

    # plant = Plant.query.get(plant_id)

    return render_template("addgarden.html") #pass through infoplant_id)


@app.route("/addplant", methods=['GET', 'POST'])
def add_plant():
    """Select a plant to add to one of your gardens"""
    if request.method == 'POST':
        if not request.form["plants"] or not request.form["planted_date"] or not request.form["garden"]:

            flash("Please enter all the fields", "error")

        else:
            garden_id = int(request.args.get("garden"))
            garden = Garden.query.get(garden_id)

            plant_id = int(request.args.get("plants"))
            plant = Plant.query.get(plant_id)

            planted_date = request.form("planted_date")

            harvest_date = calculate_harvest_date(plant_id, planted_date)

            new_gardenplant_obj = GardenPlants(garden_id=garden_id,
                                               plant_id=plant.plant_id,
                                               planted_date=planted_date,
                                               harvest_date=harvest_date)

            db.session.add(new_gardenplant_obj)
            db.session.commit()

            flash("{} successfully added to {}".format(plant.pname, garden.garden_name))
            return redirect("/mygarden", plant=plant)

             # <select name="plants">
    return render_template("add_plant.html")



    # --POST:
    # page will show form with drop down plant list like from homepage
    # form will have an optional planted date input
    # form will have a chance to override harvest_date?

    # post route needs calculate_harvest_date function
    # form inputs will add that info to the database as a new gardenplants object
    # once submitted, event listener prompt to add another plant (Y/N)
    # would be nice to have a link to not just add plant to garden, but
    # add plant to a "favorites" list
        # create object, will need to supply inputs, in order to supply
        # harvest_date, will need to call ClassName.calculate_harvest_date 
        # and store in a variable, then can pass that variable to database
        # when entry is created
    # return render_template("addplants.html", #pass through info)


@app.route("/editgarden", methods='GET', 'POST')
def edit_garden():
    """add, remove, or change gardens and/or plant information in db"""

    return render_template("editgarden.html")

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
