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

    if request.args.get("plants"):
        plant_id = int(request.args.get("plants"))
        plant = Plant.query.get(plant_id)
    else:
        flash("Select a plant to find out more")
        return redirect("/")
    # test 1: with a specific plant_id - output contains name or something
    # plants ?=foobar >>>> 404 page with photo, can't find your plant info or a bad request result or redirect with flash message
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

# test kwargs with getting text from variables
# put request.form lin and datetime.now in new_user instanciation?

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
        flash("Invalid credentials")
        return redirect("/login")

    if user.password != password:
        flash("Invalid credentials")
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
            # if statement if date format doesn't match line above this one
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


@app.route("/frostdates_demo", methods=['GET', 'POST'])
def show_frost_demo():

    user = User.query.get(session['user_id'])

    return render_template("frostdates_demo.html", user=user)
@app.route("/create_event", methods=['POST'])
def create_event():

    POST https://www.googleapis.com/calendar/v3/calendars/calendarId/events

####################################### FROM API EXERCISE
@app.route("/create-event", methods=['POST'])
def create_eventbrite_event():
    """Create Eventbrite event using form data"""

    name = request.form.get('name')
    # The Eventbrite API requires the start & end times be in ISO8601 format
    # in the UTC time standard. Adding ':00' at the end represents the seconds,
    # and the 'Z' is the zone designator for the zero UTC offset.
    start_time = request.form.get('start-time') + ':00Z'
    end_time = request.form.get('end-time') + ':00Z'
    timezone = request.form.get('timezone')
    currency = request.form.get('currency')

    payload = {'event.name.html': name,
               'event.start.utc': start_time,
               'event.start.timezone': timezone,
               'event.end.utc': end_time,
               'event.end.timezone': timezone,
               'event.currency': currency,
               }

    # The token can't be sent as part of the payload for POST requests to
    # Eventbrite's API and must be sent as part of the header instead
    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.post(EVENTBRITE_URL + "events/",
                             data=payload,
                             headers=headers)
    data = response.json()

    # If the response was successful, redirect to the homepage
    # and flash a success message
    if response.ok:
        flash(f"Your event was created! Here's the link: {data['url']}")
        return redirect("/")

    # If the response was an error, redirect to the event creation page
    # and flash a message with the error description from the returned JSON
    else:
        flash(f"Error: {data['error_description']}")
        return redirect("/create-event")
#########################################

# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

event = {
  'summary': 'Test Harvest Time',
  'location': 'GARDEN XYZ',
  'description': 'ABC is probably ready to harvest',
  'start': {
    'dateTime': '2018-09-24T00:00:00-00:00'
  },
  'end': {
    'dateTime': '2018-10-01T17:00:00-07:00'
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ]
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

event = service.events().insert(calendarId='primary', body=event).execute()
print('Event created: {}'.format(event.get('htmlLink')))

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
