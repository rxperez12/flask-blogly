from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbx = db.session.execute

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
        db.String(100)
    )

    def get_full_name(self):
        """Returns first name and last name as a string spearated by a space
        """
        return f'{self.first_name} {self.last_name}'
