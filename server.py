"""Garden Plants."""
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
import requests
from sqlalchemy.orm import exc
# from flask_login import login_required, current_user (Phase 2?)
from datetime import datetime, timedelta

from model import connect_to_db, db, Plant, User, UserGarden, Water, Sun, GardenPlants
#ZipFrostDate

from utils import is_user_by_username, is_email_by_email

from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery
import httplib2


# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

GOOGLE_CALENDAR_API_POST_URL = 'https://www.googleapis.com/calendar/v3/calendars/primary/events?sendNotifications=true&key=AIzaSyDPku5RTnykujA8vcvC7h8fNP1KMD-tVLI'

app = Flask(__name__)

app.secret_key = 'abc'

app.jinja_env.undefined = StrictUndefined


def create_gardenplants_calendar_payload(gardenplants_id):

    gardenplant = GardenPlants.query.get(gardenplants_id)

    harvest_start_date = gardenplant.harvest_date
    harvest_end_date = gardenplant.harvest_date + timedelta(days=7)

    harvest_start_date_string = datetime.strftime(harvest_start_date, '%Y-%m-%d')
    harvest_end_date_string = datetime.strftime(harvest_end_date, '%Y-%m-%d')

    gardenplant_payload = {"summary": "Harvest Time:{}".format(gardenplant.plant.pname),
                           "location": "{}".format(gardenplant.gardens.garden_name),
                           "start": {"date": harvest_start_date_string},
                           "end": {"date": harvest_end_date_string},
                           "description": ("{} plant(s) ready!".format(gardenplant.plant.pname)),
                           "reminders": {"useDefault": True}
                           }

    return gardenplant_payload


@app.route('/', methods=['GET'])
def index():
    """Homepage."""

    plants = db.session.query(Plant).order_by('pname').all()

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

    return render_template("plant.html", plant=plant)


@app.route("/validate_user_reg.json")
def validate_user_email():
    """Return results of username, email lookup in db."""

    username = request.args.get("username")
    email = request.args.get("email")

    validation_info = {
        'username_validation': is_user_by_username(username),
        'email_validation': is_email_by_email(email)
    }

    return jsonify(validation_info)


@app.route('/register', methods=['GET', 'POST'])
def process_registration():
    """Render page and process user registration."""

    if session:
        flash("You are already logged in.")
        return redirect("/")

    if request.method == 'POST':
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        zipcode = request.form["zipcode"]

        if is_user_by_username(username):
            flash("")
            return redirect("/login")

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

    return render_template("new_user.html")


@app.route('/login', methods=['GET', 'POST'])
def process_login():
    """Render login form page and process login."""

    if request.method == 'POST':
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

    return render_template("/login.html")


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


@app.route('/saveharvestevent', methods=['POST'])
def store_harvest_info_for_api():

    if session['user_id']:

        gardenplants_id = request.form['gardenplants_id']
        print("------------------print(gardenplants_id")
        print(gardenplants_id)
        session['gardenplants_id'] = gardenplants_id
        print("-------------------print(session5)")
        print(session)
        return redirect('/add-harvest-to-calendar')

    return redirect("/login")


@app.route('/add-harvest-to-calendar', methods=['GET'])
def add_harvest_to_calendar():

    if 'credentials' not in session:
    # user has not authorized this app yet

        return redirect('authorize')

    else:
        payload = create_gardenplants_calendar_payload(session['gardenplants_id'])

        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        # Load credentials from the session.

        session['credentials'] = credentials_to_dict(credentials)
        # Save credentials back to session in case access token was refreshed.
        # ACTION ITEM: In a production app, you likely want to save these
        # credentials in a persistent database instead.

        service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

        event = service.events().insert(calendarId='primary', body=payload).execute()

        flash("Your event was created! Here's the link: {}".format(event.get('htmlLink')))
        session.pop('gardenplants_id', None)

        return redirect("/mygarden")


@app.route('/authorize')
def authorize():
    # LAST INTERACTION WITH USER BEFORE GOING TO GOOGLE
    # CAN BE RENAMED TO CLARIFY WHO IS AUTHORIZING
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    session['state'] = state
    # Store the state so the callback can verify the auth server response.

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # USER HAS AUTHORIZED MY APP AND GOOGLE IS SENDING THAT APPROVAL BACK
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('add_harvest_to_calendar'))


@app.route('/revoke')
def revoke():
    if 'credentials' not in session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')

    if status_code == 200:
        return('Credentials successfully revoked.' + print_index_table())
    else:
        return('An error occurred.' + print_index_table())


@app.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']
    return ('Credentials have been cleared.<br><br>' +
            print_index_table())


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def print_index_table():
    return ('<table>' +
            '<tr><td><a href="/test">Test an API request</a></td>' +
            '<td>Submit an API request and see a formatted JSON response. ' +
            '    Go through the authorization flow if there are no stored ' +
            '    credentials for the user.</td></tr>' +
            '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
            '<td>Go directly to the authorization flow. If there are stored ' +
            '    credentials, you still might not be prompted to reauthorize ' +
            '    the application.</td></tr>' +
            '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
            '<td>Revoke the access token associated with the current user ' +
            '    session. After revoking credentials, if you go to the test ' +
            '    page, you should see an <code>invalid_grant</code> error.' +
            '</td></tr>' +
            '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
            '<td>Clear the access token currently stored in the user session. ' +
            '    After clearing the token, if you <a href="/test">test the ' +
            '    API request</a> again, you should go back to the auth flow.' +
            '</td></tr></table>')


if __name__ == "__main__":

    app.debug = False

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
