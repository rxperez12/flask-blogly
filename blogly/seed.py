"""Seed movies db with data."""

from app import app
from models import db, User, Post

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
taylor = Post(
    title = "It's me",
    content = "Hi, I'm the problem it's me",
    user_id = 1
)

funny = Post(
    title = 'What does a nosey pepper do?',
    content = 'It gets jalapeño business.',
    user_id = 1
)

true = Post(
    title = 'SQL: Why it is the worst',
    content = "It's so obvious anyone can see that. I don't even need a reason.",
    user_id = 2
)



db.session.add_all([rob, john, funny, true, taylor])
db.session.commit()


