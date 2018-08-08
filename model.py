"""Models and database functions for Garden Web App project."""
from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta

db = SQLAlchemy()


class User(db.Model):
    """User of garden website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(16), nullable=False)
    lname = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    zipcode = db.Column(db.String(15), nullable=False)
    reg_date = db.Column(db.DateTime)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} email={}>".format(self.user_id, self.email)


class UserGarden(db.Model):
    """Plant water categories"""

    __tablename__ = "usergarden"

    garden_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    garden_name = db.Column(db.String(48), nullable=False)
    garden_desc = db.Column(db.String(48), nullable=False)
    sun_id = db.Column(db.Integer, db.ForeignKey('sun.sun_id'))

    user = db.relationship("User", backref="usergarden")
    sun = db.relationship("Sun", backref="usergarden")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Garden_id={} garden name={}>".format(self.garden_id, self.garden_name)


class GardenPlants(db.Model):
    """Plant water categories"""

    __tablename__ = "gardenplants"

    gardenplants_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    garden_id = db.Column(db.Integer, db.ForeignKey('usergarden.garden_id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.plant_id'))
    planted_date = db.Column(db.DateTime, nullable=False)
    harvest_date = db.Column(db.DateTime, nullable=False)
    gardens = db.relationship("UserGarden", backref="gardenplants")
    plant = db.relationship("Plant", backref="gardenplants")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Gardenplants_id={}>".format(self.gardenplants_id)

    @staticmethod
    def calculate_harvest_date(plant_id, planted_date):
        """Return harvest date for gardenplant"""

        plant = Plant.query.get(plant_id)
        harvest_date = planted_date + timedelta(days=plant.pdays_to_harvest)
        return harvest_date


class Plant(db.Model):
    """Plants for garden website."""

    __tablename__ = "plant"

    plant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pname = db.Column(db.String(100))
    pdescription = db.Column(db.String(200))
    water_id = db.Column(db.Integer, db.ForeignKey('water.water_id'))
    sun_id = db.Column(db.Integer, db.ForeignKey('sun.sun_id'))
    pdays_to_harvest = db.Column(db.Integer, nullable=False)
    pspacing = db.Column(db.String, nullable=True)
    prow_spacing = db.Column(db.String, nullable=True)
    plant_note = db.Column(db.String(250), nullable=True)

    sun = db.relationship("Sun", backref="plant")
    water = db.relationship("Water", backref="plant")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Plant_id={} plant name={}>".format(self.plant_id, self.pname)


class Sun(db.Model):
    """Sun exposure category for plant."""

    __tablename__ = "sun"

    sun_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sun_name = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Sun sun_id={} sun name={}>".format(self.sun_id, self.sun_name)


class Water(db.Model):
    """Plant water categories"""

    __tablename__ = "water"

    water_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    water_name = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Water_id={} water name={}>".format(self.water_id, self.water_name)


# Phase 2 potentially


class ZipFrostDate(db.Model):
    """Frost dates by zipcode categories"""

    __tablename__ = "zipfrost_date"

    zipfrost_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    zipfrost_code = db.Column(db.Integer, nullable=False)
    fallfrost_date = db.Column(db.DateTime, nullable=False)
    springfrost_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Zipfrost_id={} zipfrost_code={}.>".format(self.zipfrost_id, self.zipfrost_code)


######## HELPER FUNCTIONS #####################################################

def connect_to_db(app, url='postgresql:///plants'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)

    print("Connected to DB.")
