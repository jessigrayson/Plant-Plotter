from unittest import TestCase, main

from server import app
from model import db, connect_to_db


class NotLoggedInNavigationTests(TestCase):
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

    def test_login_page(self):
        """Test login page renders properly"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h1>Login</h1>", result.data)
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
        self.assertIn(b"""<form action="/register">
                      <input type="submit" value="Register">""",
                      result.data)

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
        self.assertEqual(result.status_code, 302)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_plant_page(self):
        """Tests user redirected home if /plant (url hack) when not logged in"""

        result = self.client.get("/plant", follow_redirects=True)
        self.assertEqual(result.status_code, 302)
        self.assertIn(b"Select a plant to find out more")
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

####################### TEST-DRIVEN-DEVELOPMENT #############################
    def test_edit_garden_page(self):
        """Tests user redirected to /login if /edit_garden (url hack) when not logged in"""
        
        result = self.client.get("/edit_garden", follow_redirects=True)
        self.assertEqual(result.status_code, 302)
        self.assertIn(b"You must be logged in to edit your garden", result.data)
        self.assertIn(b"Login", result.data)
        self.assertNotIn(b"Logout", result.data)

    def test_
if __name__ == "__main__":
    unittest.main()
