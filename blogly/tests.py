import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"
os.environ["FLASK_DEBUG"] = "0"

from models import db, dbx, DEFAULT_IMAGE_URL, User, Post
from app import app
from unittest import TestCase


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
assert app.config['SQLALCHEMY_DATABASE_URI'] == "postgresql:///blogly_test"
app.app_context().push()
db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        dbx(db.delete(User))
        db.session.commit()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        test_post = Post(
            title="test_title1",
            content="I DID IT SUCCESS",
            user_id = test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Test whether page lists users"""
        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_user(self):
        """Test whether user appears with first and last name"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test1_first', html)
            self.assertIn('<!-- User detail comment for testing -->', html)

    def test_add_user(self):
        """Test if user can be successfully added"""

        with app.test_client() as client:
            user = {
                "first_name": "test3_first",
                "last_name": "test3_last",
                "image_url": DEFAULT_IMAGE_URL
            }

            resp = client.post('/users/new', data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test3_first', html)


    def test_add_post(self):
        """Test if post can be successfully added"""

        with app.test_client() as client:
            post = {
                "title": "test_title2",
                "content": "test_content2",
                "user_id": "1"
            }

            resp = client.post(f'/users/{self.user_id}/posts/new', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_title2', html)

    def test_remove_post(self):
        """Test if post can be successfully removed"""

        with app.test_client() as client:

            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('I DID IT SUCCESS', html)


