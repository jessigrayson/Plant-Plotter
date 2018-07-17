"""Models and database functions for Garden Web App project."""
from flask_sqlalchemy import SQLAlchemy
# from collections import defaultdict

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

########## USER CLASS ############

class User(db.Model):
    """User of garden website."""

    __tablename__ = "user"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(16), nullable=False)
    lname = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)
    reg_date = db.Column(db.DateTime)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={self.user_id} email={self.email}>"


########## USER-GARDEN CLASS ############


class UserGarden(db.Model):
    """Plant water categories"""

# SHOULD I MAKE GARDEN LOCATION A BOOLEAN?

    __tablename__ = "usergarden"

    garden_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    garden_name = db.Column(db.String(48), nullable=False)
    garden_desc = db.Column(db.String(48), nullable=False)
    sun_id = db.Column(db.Integer, db.ForeignKey('sun.sun_id'))

    user = db.relationship("User", backref="usergarden")
    sun = db.relationship("Sun", backref="usergarden")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Garden_id={self.garden_id} garden name={self.garden_name}.>"""


class Plant(db.Model):
    """Plants for garden website."""
# DO WE NEED TO SPECIFY NULLABLE ON EACH ONE?
# HOW TO MAKE PLANT CLASS WITH ADDITIONAL ATTRIBUTES SPECIFIC TO
# THAT GARDEN'S USER LOCATION?

# WHAT METRIC FOR SPACING?

# PLANT PHOTO CONSTRUCT FOR CONSTRUCTING DB

    __tablename__ = "plant"

    plant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pname = db.Column(db.String(100))
    pdescription = db.Column(db.String(200))
    water_id = db.Column(db.Integer, db.ForeignKey('water.water_id'))
    sun_id = db.Column(db.Integer, db.ForeignKey('sun.sun_id'))
    pdays_to_harvest = db.Column(db.Integer, nullable=False)
    pspacing = db.Column(db.Integer, nullable=True)
    prow_spacing = db.Column(db.Integer, nullable=True)
    plant_note = db.Column(db.String(250), nullable=True)

    sun = db.relationship("Sun", backref="plant")
    water_id = db.relationship("Water", backref="plant")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Plant_id={self.plant_id} plant name={self.pname}.>"""


class UserPlanted(db.Model):
    """Plant water categories"""

# SHOULD I MAKE GARDEN LOCATION A BOOLEAN?

    __tablename__ = "userplanted"

    userplanted_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.plant_id'))
    planted_date = db.Column(db.DateTime)

    user = db.relationship("User", backref="userplanted")
    plant = db.relationship("Plant", backref="userplanted")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Userplanted_id={self.userplanted_id}.>"""


class Sun(db.Model):
    """Sun exposure category for plant."""

    __tablename__ = "sun"

    sun_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sun_name = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Sun sun_id={self.sun_id} sun name={self.sun_name}.>"""


class Water(db.Model):
    """Plant water categories"""

    __tablename__ = "water"

    water_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    water_name = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Water_id={self.water_id} water name={self.water_name}.>"""


class ZipFrostDate(db.Model):
    """Frost dates by zipcode categories"""

# SHOULD I MAKE GARDEN LOCATION A BOOLEAN?

    __tablename__ = "zip_frost_date"

    zipfrost_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    zipfrost_code = db.Column(db.Integer, nullable=False)
    fall_frost_date = db.Column(db.DateTime, nullable=False)
    sprint_frost_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Zipfrost_id={self.zipfrost_id} zipfrost_code={self.zipfrost_code}.>"""


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///plants'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)

    print("Connected to DB.")
