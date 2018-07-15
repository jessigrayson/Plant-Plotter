"""Utility file to seed plant database from Plant data in seed_data/"""

import datetime
from sqlalchemy import func

from model import Plant, User, UserGarden, Sun, Water, ZipFrostDate, UserPlantconnect_to_db, db
from server import app


def load_plants(plant_filename):
    """Load plants from plants file into database."""

    print("Plants")

    for i, row in enumerate(open(plant_filename)):
        row = row.rstrip()

        plant_id, pname, pdescription, water_id, sun_id, pdays_to_harvest, pspacing, prow_spacing = row.split(",")

        plant = Plant(plant_id=plant_id,
                      pname=pname,
                      pdescription=pdescription,
                      water_id=water_id,
                      sun_id=sun_id,
                      pdays_to_harvest=pdays_to_harvest,
                      pspacing=pspacing,
                      prow_spacing=prow_spacing,
                      p_note=p_note)

        # # We need to add to the session or it won't ever be stored
        db.session.add(plant)

    db.session.commit()


def load_user(user_filename):
    """Load users from users file into database."""

    print("User")

    for i, row in enumerate(open(user_filename)):
        row = row.rstrip()

        user_id, username, password, fname, lname, email, zipcode, reg_date_str = row.split(",")

        if reg_date_str:
            reg_date = datetime.datetime.strptime(reg_date_str, "%m/%d/%Y")
        else:
            reg_date = None

        user = User(user_id=user_id,
                    username=username,
                    password=password,
                    fname=wfname,
                    lname=lname,
                    email=email,
                    zipcode=zipcode,
                    reg_date=reg_date)

        db.session.add(user)

    db.session.commit()


def load_sun(sun_filename):
    """Load sun data from sun file into database."""

    print("Sun")

    for i, row in enumerate(open(sun_filename)):
        row = row.rstrip()

        sun_id, sun_name = row.split(",")

        sun = Sun(sun_id=sun_id,
                  sun_name=sun_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(sun)

    db.session.commit()


def load_water(water_filename):
    """Load water from water file into database."""

    print("Water")

    for i, row in enumerate(open(water_filename)):
        row = row.rstrip()

        water_id, water_name = row.split(",")

        water = Water(water_id=sun_id, 
                    water_name=water_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    db.session.commit()


def load_usergarden(usergarden_filename):
    """Load user garden from usergarden file into database."""

    print("User Garden")

    for i, row in enumerate(open(usergarden_filename)):
        row = row.rstrip()

        garden_id, user_id, garden_name, garden_description, sun_id = row.split(",")

        usergarden = UserGarden(garden_id=garden_id,
                    user_id=user_id,
                    garden_name=garden_name, 
                    garden_description=garden_description, 
                    sun_id=sun_id)

        # # We need to add to the session or it won't ever be stored
        db.session.add(usergarden)

    db.session.commit()


def load_userplanted(userplanted_filename):
    """Load user plants from userplanted file into database."""

    print("User Plants")

    for i, row in enumerate(open(userplanted_filename)):
        row = row.rstrip()

        userplanted_id, user_id, plant_id, planted_date_str = row.split(",")

        if planted_date_str:
            planted_date = datetime.datetime.strptime(planted_date_str, "%m/%d/%Y")
        else:
            planted_date = None

        userplanted = UserPlanted(userplanted_id=userplanted_id,
                                  user_id=user_id,
                                  plant_id=plant_id,
                                  planted_date=planted_date)

        # We need to add to the session or it won't ever be stored
        db.session.add(userplanted)

    db.session.commit()


def load_zip_frost_date(zipfrostdate_filename):
    """Load user plants from userplanted file into database."""

    print("Zip Frost Date")

    for i, row in enumerate(open(zipfrostdate_filename)):
        row = row.rstrip()

        zip_frost_id, zip_frost_code, fall_frost_date_str, spring_frost_date_str = row.split(",")

        if fall_frost_date_str:
            fall_frost_date = datetime.datetime.strptime(fall_frost_date_str, "%m/%d/%Y")
        else:
            fall_frost_date = None

        if spring_frost_date_str:
            spring_frost_date = datetime.datetime.strptime(string_frost_date_str, "%m/%d/%Y")
        else:
            spring_frost_date = None

        zip_frost_date = ZipFrostDate(zip_frost_id=zip_frost_id,
                                      zip_frost_code=zip_frost_code,
                                      fall_frost_date=fall_frost_date,
                                      spring_frost_date=spring_frost_date)

        # We need to add to the session or it won't ever be stored
        db.session.add(zipfrostdate)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

plant_filename = "seed/plants"
user_filename = "seed/user"
sun_filename = "seed/sun"
water_filename = "seed/water"
usergarden_filename = "seed/usergarden"
userplanted_filename = "seed/userplanted"
zipfrostdate_filename = "seed/zipfrostdates"

load_plants(plant_filename)
load_user(user_filename)
load_sun(sun_filename)
load_water(water_filename)
load_usergarden(usergarden_filename)
load_userplanted(userplanted_filename)
load_zip_frost_date(zipfrostdate_filename)
set_val_user_id()