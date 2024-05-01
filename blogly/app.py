"""Blogly application."""

from flask import Flask, request, redirect, render_template
import os
from models import db, dbx, User
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import NotFound


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "shhh-secret")


debug = DebugToolbarExtension(app)


@app.get('/')
def homepage():

    return render_template('base.jinja')
