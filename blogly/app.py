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
    """TODO: WIP - Redirect to list of users"""
    return render_template('base.jinja')


@app.get('/users')
def display_users():
    """Show all users sorted alphabetically"""

    return render_template('user_listing.jinja')


@app.get('/users/new')
def display_add_form():
    """Show add form for users"""
    return render_template("new_user_form.jinja")


@app.post('/users/new')
def handle_form_entry():
    """Process the add form, add new user and redirects to /users"""
    return redirect('/users')


@app.get('/users/int:<user_id>')
def display_specific_user(user_id):
    """Show information about the given user"""
    return render_template('user_details.jinja', 'TODO:')


@app.get('/users/int:<user_id>/edit')
def display_specific_user_edit(user_id):
    """Show show the edit page for a given user"""
    return render_template('edit_user.jinja', 'TODO:')


@app.post('/users/int:<user_id>/edit')
def handle_user_edit(user_id):
    """Process edit form then redirect to /users page"""
    return redirect('/users')


@app.post('/users/int:<user_id>/delete')
def handle_user_delete(user_id):
    """Delete the user then redirect to /users page"""
    return redirect('/users')
