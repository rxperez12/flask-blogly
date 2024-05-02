"""Blogly application."""

from flask import Flask, request, redirect, render_template
import os
from models import db, dbx, User, DEFAULT_IMAGE_URL
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

    return redirect('/users')


@app.get('/users')
def display_users():
    """Show all users sorted alphabetically"""

    q_users = db.select(User).order_by(User.last_name, User.first_name)
    users = dbx(q_users).scalars().all()

    return render_template('users_list.jinja', users=users)


@app.get('/users/new')
def display_add_form():
    """Show add form for users"""

    return render_template("new_user_form.jinja")


@app.post('/users/new')
def handle_new_user_entry():
    """Process the add form, add new user and redirects to /users"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or DEFAULT_IMAGE_URL

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
    # user = db.one_or_404(User, user_id)  # easier because does both rows above

    return render_template('user_details.jinja', user=user)


@app.get('/users/<int:user_id>/edit')
def display_specific_user_edit(user_id):
    """Show show the edit page for a given user"""

    q_user = db.select(User).where(User.id == user_id)
    user = db.one_or_404(q_user)
    # user = db.one_or_404(User, user_id)  # easier because does both rows above

    return render_template('edit_user.jinja', user=user)


@app.post('/users/<int:user_id>/edit')
def handle_user_edit(user_id):
    """Process edit form then redirect to /users page"""

    q_user = db.select(User).where(User.id == user_id)
    user = db.one_or_404(q_user)
    # user = db.get_or_404(User, user_id)  # easier because does both rows above

    user.first_name = request.form['first_name'] or user.first_name
    user.last_name = request.form['last_name'] or user.last_name
    user.image_url = request.form['image_url'] or DEFAULT_IMAGE_URL

    db.session.commit()
    return redirect('/users')

    # IS THERE A WAY TO GET THIS TO WORK???? - NOT GOOD IDEA / REALLY BAD IDEA
    # for key, value in request.form.items():
    #     if (value):
    #         user[key] = value - stupid doesn't work


@app.post('/users/<int:user_id>/delete')
def handle_user_delete(user_id):
    """Delete the user then redirect to /users page"""

    user = db.get_or_404(User, user_id)
    db.session.delete(user)

    db.session.commit()

    return redirect('/users')
