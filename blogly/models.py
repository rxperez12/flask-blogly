from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbx = db.session.execute


DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"

"""Models for Blogly."""


class User (db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True
    )

    first_name = db.mapped_column(
        db.String(50),
        nullable=False
    )

    last_name = db.mapped_column(
        db.String(50),
        nullable=False
    )

    image_url = db.mapped_column(
        db.String(),
        default=DEFAULT_IMAGE_URL,
        nullable=True
        #TODO: Empty string better for nothing. Default - equals url, nullable = False - Always on creation, handle edit
    )

    def get_full_name(self): #property could be a good solution in the future
        """Returns first name and last name as a string spearated by a space
        """
        return f'{self.first_name} {self.last_name}'

    posts = db.relationship(
        'Post',
        back_populates='user',
        cascade='all, delete-orphan'
    )


class Post(db.Model):
    """Model"""

    __tablename__ = 'post'

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True
    )

    title = db.mapped_column(
        db.String(50),
        nullable=False
    )

    content = db.mapped_column(
        db.String(),
        nullable = False
    )

    created_at = db.mapped_column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    user = db.relationship(
        "User",
        back_populates='posts',
        cascade="all, delete-orphan"
    )


