"""Seed movies db with data."""

from app import app
from models import db, User

app.app_context().push()

db.drop_all()
db.create_all()

rob = User(
    first_name="Rob",
    last_name='Stone',
    image_url='https://t.ly/6BWd_'
)
john = User(
    first_name="John",
    last_name='Smith',
)

db.session.add_all([rob, john])
db.session.commit()
