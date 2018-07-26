import unittest

from server import app
from model import db, example_data, connect_to_db

class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()

        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Garden Tracker", result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"username": "jenjen", "password": "jenjen3"},
                                  follow_redirects=True)
        self.assertIn(b"Jen Indoor Garden", result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_new_user(self):
        """Test creation of new user"""

        result = self.client.post("/register",
                                  data={"fname": "John",
                                        "lname": "Testerman",
                                        "email": "johnappleseed@gmail.com",
                                        "username": "johntest",
                                        "password": "testpassword",
                                        },
                                  follow_redirects=True)
        self.assertIn(b"User johntest added", result.data)


    def test_games(self):
        """Test departments page."""

        result = self.client.get("/games")
        self.assertIn(b"Power Grid", result.data)
