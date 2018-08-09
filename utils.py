
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import exc
# from flask_login import login_required, current_user (Phase 2?)
from datetime import datetime

from model import db, Plant, User, UserGarden, Water, Sun, GardenPlants


def is_user_by_username(username):
    """Return True is username exists in db."""

    try:
        # user = User.query.filter(User.username == username).one()
        # if user:
        username_check = db.session.query(User.username == username).one()
        if username_check:
            return True

    except exc.MultipleResultsFound or exc.NoResultFound:
        return False


def is_email_by_email(email):
    """Return True is email exists in db."""

    try:
        # email = User.query.filter(User.email == email).one()
        # if email:
        email_check = db.session.query(User.email == email).one()
        if email_check:
            return True

    except exc.MultipleResultsFound or exc.NoResultFound:
        return False
