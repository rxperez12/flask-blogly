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
    q_users = db.select(User).order_by(User.first_name)
    users = dbx(q_users).scalars().all()

    return render_template('user_listing.jinja', users=users)


@app.get('/users/new')
def display_add_form():
    """Show add form for users"""
    return render_template("new_user_form.jinja")


@app.post('/users/new')
def handle_new_user_entry():
    """Process the add form, add new user and redirects to /users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )

    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.get('/users/<int:user_id>')
def display_specific_user(user_id):
    """Show information about the given user"""

    q_user = db.select(User).where(User.id == user_id)
    user = db.one_or_404(q_user)

    return render_template('user_details.jinja', user=user)


@app.get('/users/<int:user_id>/edit')
def display_specific_user_edit(user_id):
    """Show show the edit page for a given user"""

    q_user = db.select(User).where(User.id == user_id)
    user = db.one_or_404(q_user)

    return render_template('edit_user.jinja', user=user)


@app.post('/users/<int:user_id>/edit')
def handle_user_edit(user_id):
    """Process edit form then redirect to /users page"""

    q_user = db.select(User).where(User.id == user_id)
    user = db.one_or_404(q_user)

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    if (first_name):
        user.first_name = first_name
    elif (last_name):
        user.last_name = last_name
    elif (image_url):
        user.image_url = image_url

    db.session.commit()
    return redirect('/users')

    # IS THERE A WAY TO GET THIS TO WORK????
    # for key, value in request.form.items():
    #     if (value):
    #         user[key] = value - stupid doesn't work


@app.post('/users/<int:user_id>/delete')
def handle_user_delete(user_id):
    """Delete the user then redirect to /users page"""
    return redirect('/users')
