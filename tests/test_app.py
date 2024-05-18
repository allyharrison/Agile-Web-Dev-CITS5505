import unittest
import sys
import os
 
# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
from app import app, db
from app.models import User, Post, Comment, Message
from flask import url_for
from flask_testing import TestCase
 
class BasicTests(TestCase):
 
    def create_app(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory SQLite database
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF protection for testing
        app.config['SECRET_KEY'] = 'test-secret-key' # Set a secret key for sessions
        return app
 
    def setUp(self):
        # Set up the database with some initial data
        db.create_all() # Create all database tables
        user1 = User(username='testuser1', email='test1@example.com')
        user1.set_password('password')
        user2 = User(username='testuser2', email='test2@example.com')
        user2.set_password('password')
        db.session.add(user1) # Add user1 to the database session
        db.session.add(user2) # Add user2 to the database session
        db.session.commit() # Commit the session to the database
 
    def tearDown(self):
        # Tear down the database after each test
        db.session.remove() # Remove the session
        db.drop_all() # Drop all database tables
 
    def test_register_user(self):
        # Test user registration
        response = self.client.post(url_for('register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 302) # Check if redirect happened after registration
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user) # Verify that the new user was created
   
    def test_login_user(self):
        # Test user login
        response = self.client.post(url_for('login'), data={
            'username': 'testuser1',
            'password': 'password'
        }, follow_redirects=True)
        self.assertIn(b'Profile', response.data) # Check if 'Profile' is in the response data
        user = User.query.filter_by(username='testuser1').first()
        self.assertIsNotNone(user)   # Verify that the user exists
   
    def test_edit_profile(self):
        # Test editing the profile
        self.login('testuser1', 'password') # Log in the user
        response = self.client.post(url_for('edit_profile'), data={
            'username': 'updateduser',
            'about_me': 'This is an updated bio'
        }, follow_redirects=True)
        self.assertIn(b'Your changes have been saved.', response.data) # Check if the success message is present
        user = User.query.filter_by(username='updateduser').first()
        self.assertIsNotNone(user) # Verify that the username was updated
        self.assertEqual(user.about_me, 'This is an updated bio') # Check if the bio was updated
   
    def test_create_post(self):
        # Test creating a new post
        self.login('testuser1', 'password') # Log in the user
        response = self.client.post(url_for('index'), data={
            'post': 'This is a test post'
        }, follow_redirects=True)
        self.assertIn(b'Your post is now live!', response.data) # Check if the success message is present
        post = Post.query.filter_by(body='This is a test post').first()
        self.assertIsNotNone(post) # Verify that the post was created
   
    def test_create_comment(self):
        # Test creating a comment on a post
        self.login('testuser1', 'password')
        post = Post(body='Test post', author=User.query.filter_by(username='testuser1').first())
        db.session.add(post) # Add the post to the session
        db.session.commit() # Commit the session to the database
        response = self.client.post(url_for('comment'), data={
            'content': 'This is a test comment',
            'post_id': post.id
        }, follow_redirects=True)
        self.assertIn(b'Your comment has been posted!', response.data) # Check if the success message is present
        comment = Comment.query.filter_by(content='This is a test comment').first()
        self.assertIsNotNone(comment) # Verify that the comment was created
   
    def test_follow_unfollow(self):
        # Test following and unfollowing a user
        self.login('testuser1', 'password')
        user2 = User.query.filter_by(username='testuser2').first()
       
        # Follow user2
        response = self.client.post(url_for('follow', username='testuser2'), data={}, follow_redirects=True)
        self.assertIn(b'You are following testuser2!', response.data)
        self.assertTrue(User.query.filter_by(username='testuser1').first().is_following(user2))
       
        # Unfollow user2
        response = self.client.post(url_for('unfollow', username='testuser2'), data={}, follow_redirects=True)
        self.assertIn(b'You are not following testuser2.', response.data)
        self.assertFalse(User.query.filter_by(username='testuser1').first().is_following(user2))
   
    def test_send_message(self):
        # Test sending a message to another user
        self.login('testuser1', 'password')
        response = self.client.post(url_for('send_message', recipient='testuser2'), data={
            'message': 'Hello, testuser2!'
        }, follow_redirects=True)
        self.assertIn(b'Your message has been sent.', response.data)  # Check if the success message is present
        message = Message.query.filter_by(body='Hello, testuser2!').first()
        self.assertIsNotNone(message) # Verify that the message was created
   
    def test_translation(self):
        # Test the text translation feature
        self.login('testuser1', 'password')
        response = self.client.post(url_for('translate_text'), json={
            'text': 'Hello',
            'source_language': 'en',
            'dest_language': 'es'
        })
        self.assertEqual(response.status_code, 200) # Check if the request was successful
        self.assertIn('Hola', response.json['text']) # Verify the translation
 
    def login(self, username, password):
        # Helper method to log in a user
        return self.client.post(url_for('login'), data={
            'username': username,
            'password': password
        }, follow_redirects=True)
 
if __name__ == '__main__':
    unittest.main() # Run the tests