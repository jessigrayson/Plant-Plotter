
from server import app
from model import db, connect_to_db

from unittest import TestCase, main
from datetime import datetime, timedelta
from unittest.mock import patch
from flask import session


class UserNotLoggedInNavigationTests(TestCase):
    """Navigation tests(no db queries) if user not logged in"""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()

    def test_homepage(self):
        """Test homepage, navbar renders text properly"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Garden Tracker</h2>", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_my_garden_page_redirect(self):
        """Test mygarden page redirects user to home correctly"""

        result = self.client.get("/mygarden", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"You need to login to view your garden", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_add_garden_page_redirect(self):
        """Test addgarden page redirects to /login, renders correctly"""

        result = self.client.get("/addgarden", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"You must be logged in to create a garden", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_add_plant_page_redirect(self):
        """Test addplant page redirects to /login, renders correctly"""

        result = self.client.get("/addplant", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"You must be logged in to add plants", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_my_account_page_redirect(self):
        """Test My Account page redirects to /login, renders correctly"""

        result = self.client.get("/user", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"You have not yet logged in.", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_login_page(self):
        """Test login page renders correctly"""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"""<input type="submit" value="Register">""", result.data)

        self.assertIn(b"""<input type="submit" value="Log In">""", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_register_page(self):
        """Test register page renders correctly"""

        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"""<form action="/register" method="POST">""", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_logout_page(self):
        """Tests user redirected home if /logout (url hack) when not logged in"""

        result = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_plant_page(self):
        """Tests user redirected home if /plant (url hack) when not logged in"""

        result = self.client.get("/plant", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Select a plant to find out more", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)


class UserNotLoggedInDatabaseTests(TestCase):
    """Integration test user not logged in/db queries"""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()

    def test_register_username_exists(self):
        """Test user not registered if username already registered"""

        result = self.client.post("/register", data={"name": "jen",
                                                     "lname": "jenjen3",
                                                     "email": "jen",
                                                     "username": "jenjen",
                                                     "password": "yay",
                                                     "zipcode": "95050"}, follow_redirects=True)
        self.assertIn(b"Username already exists.", result.data)
        self.assertIn(b"Login", result.data)

    def test_register_email_exists(self):
        """Test user not registered if email already registered"""

        result = self.client.post("/register", data={"name": "jen",
                                                     "lname": "jenjen3",
                                                     "email": "jenn@yourmail.com",
                                                     "username": "jesjesjes",
                                                     "password": "yay",
                                                     "zipcode": "95050"}, follow_redirects=True)
        self.assertIn(b"Email already exists.", result.data)
        self.assertIn(b"Login", result.data)

    def test_register_new_user(self):
        """Test new user registered correctly."""
        pass

    def test_login_username_incorrect(self):
        """Test redirect if username does not match login credentials in db"""

        result = self.client.post("/login", data={"username": "wrongusername",
                                                  "password": "jenjen3"}, follow_redirects=True)
        self.assertIn(b"Invalid credentials", result.data)
        self.assertEqual(result.status_code, 200)

    def test_login_password_incorrect(self):
        """Test redirect if password does not match login credentials in db"""

        result = self.client.post("/login", data={"username": "jenjen",
                                                  "password": "wrongpassword"}, follow_redirects=True)
        self.assertIn(b"Invalid credentials", result.data)
        self.assertEqual(result.status_code, 200)

    def test_plant_detail_page(self):
        """Test plant page renders correctly"""

        result = self.client.post("/plant", data={"plant_id": 2})
        self.assertIn(b"strawberry description", result.data)
        self.assertEqual(result.status_code, 200)


class LoggedInNavigationTests(TestCase):
    """Navigation tests if user logged in
    setup,
    tearDown,
    login page: sign in data sent to server
    url hacking: /login when already logged in > redirect to home & flash
    nav bar says logout while logged in - every page
    nav bar does not say login while logged in - every page
    logout: delete session
    logout: redirect to home page & flash
    logout: nav bar says login
    logout: nav bar does not say logout
    my garden: render page shows all gardens
    my garden: render page shows all plants
    """
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 3

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()

    def test_homepage_logged_in(self):
        """Test homepage, navbar renders text properly if user logged in."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Garden Tracker</h2>", result.data)
        self.assertNotIn(b"Login", result.data)
        self.assertIn(b"Logout", result.data)

    def test_my_garden_page_logged_in(self):
        """Test mygarden page renders correctly if user logged in."""

        result = self.client.get("/mygarden",)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Jen Indoor Garden", result.data)
        self.assertNotIn(b"Login", result.data)
        self.asserttIn(b"Logout", result.data)

    def test_add_garden_page_logged_in(self):
        """Test addgarden page renders correctly if user logged in."""

        result = self.client.get("/addgarden")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Garden Name:", result.data)
        self.assertIn(b"Garden Description:", result.data)
        self.assertIn(b"Logout", result.data)

    def test_add_plant_page_logged_in(self):
        """Test addplant page renders correctly if user logged in."""

        result = self.client.get("/addplant")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"part shade", result.data)
        self.assertNotIn(b"Login", result.data)
        self.assertIn(b"Logout", result.data)

    def test_my_account_page_logged_in(self):
        """Test My Account page redirects to /login, renders correctly"""

        result = self.client.get("/user")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"jenn@yourmail.com", result.data)
        self.assertNotIn(b"Login", result.data)
        self.assertIn(b"Logout", result.data)

    def test_login_page_logged_in(self):
        """Test login page redirects to mygarden if user logged in"""

        result = self.client.get("/login", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"You are already logged in.", result.data)
        self.assertNotIn(b"Login", result.data)
        self.assertIn(b"Logout", result.data)

    def test_register_page_logged_in(self):
        """Test register page redirects to homepage if user logged in."""

        result = self.client.get("/register", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"You are already logged in.", result.data)
        self.assertNotIn(b"Login", result.data)
        self.assertIn(b"Logout", result.data)

    def test_logout_if_logged_in(self):
        """Tests user logout processes correctly if user logged in."""

        result = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Logged Out.", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_plant_page_if_logged_in(self):
        """Tests user redirected if /plant (url hack) when user logged in"""

        result = self.client.get("/plant", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Select a plant to find out more", result.data)
        self.assertNotIn(b"Login", result.data)
        self.assertIn(b"Logout", result.data)


class LoggedInDatabaseTests(TestCase):
    """Integration test user signup success, signup error, user login, add garden, add plant,
    *remove garden*, *remove plant*, *change password*, *link to google calendar*,
    user logout session stuff, add plant harvest date calculation,
    add garden with same names, no names, *add plant and override harvest date*
    login page: sign in data pulled from db - right login
    login page: sign in data pulled from db - wrong username & flash
    login page: sign in data pulled from db - wrong password & flash
    login page: sign in data pulled from db - wrong username and password & flash
    #login page: sign in data pulled from db - empty fields is governed by html...
    login page: data checked in db
    register page: all data sent/rcvd by server
    same email > do now allow register
    same email > redirect to login page & flash message
    register page: same fname and lname as db > allow
    register page: same lname as db > allow
    register page: same fname as db > allow
    my account pulls data from db
    myaccount shows user data rendered correctly
    *myaccount update password pulls db correctly, changes correctly, logs in correctly*
    mygarden: the right test gardens are pulled through (all 5, should have that many tables for example)
    mygarden: harvest date calculation produces this date for these plants/garden/user_id
    addgarden: adding a garden adds it to the db
    addgarden: short name fails, non alpha fails,
    addgarden: empty text produces flash message
    addgarden: flash message of successful addition to garden
    addplant: all gardens show up in drop down
    addplant: all plants show up in dropdown
    addplant: adding a plant adds it to the db
    addplant: adding a plant produces a correct harvestdate calculation to gardenplants tables
    addplant: flash message of successful addition to garden
    """
    def test_is_email_by_email(self):
        pass

    def test_is_user_by_username(self):
        pass

####################### TEST-DRIVEN-DEVELOPMENT #############################
    def test_edit_garden_page(self):
        """Tests user redirected to /login if /edit_garden (url hack) when not logged in"""      
        result = self.client.get("/edit_garden", follow_redirects=True)
        self.assertEqual(result.status_code, 302)
        self.assertIn(b"You must be logged in to edit your garden", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)


if __name__ == "__main__":
    main()
