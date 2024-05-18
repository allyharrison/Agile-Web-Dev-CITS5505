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
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test-secret-key'
        return app
 
    def setUp(self):
        db.create_all()
        user1 = User(username='testuser1', email='test1@example.com')
        user1.set_password('password')
        user2 = User(username='testuser2', email='test2@example.com')
        user2.set_password('password')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
 
    def tearDown(self):
        db.session.remove()
        db.drop_all()
 
    def test_register_user(self):
        response = self.client.post(url_for('register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 302)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
   
    def test_login_user(self):
        response = self.client.post(url_for('login'), data={
            'username': 'testuser1',
            'password': 'password'
        }, follow_redirects=True)
        self.assertIn(b'Profile', response.data)
        user = User.query.filter_by(username='testuser1').first()
        self.assertIsNotNone(user)
   
    def test_edit_profile(self):
        self.login('testuser1', 'password')
        response = self.client.post(url_for('edit_profile'), data={
            'username': 'updateduser',
            'about_me': 'This is an updated bio'
        }, follow_redirects=True)
        self.assertIn(b'Your changes have been saved.', response.data)
        user = User.query.filter_by(username='updateduser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.about_me, 'This is an updated bio')
   
    def test_create_post(self):
        self.login('testuser1', 'password')
        response = self.client.post(url_for('index'), data={
            'post': 'This is a test post'
        }, follow_redirects=True)
        self.assertIn(b'Your post is now live!', response.data)
        post = Post.query.filter_by(body='This is a test post').first()
        self.assertIsNotNone(post)
   
    def test_create_comment(self):
        self.login('testuser1', 'password')
        post = Post(body='Test post', author=User.query.filter_by(username='testuser1').first())
        db.session.add(post)
        db.session.commit()
        response = self.client.post(url_for('comment'), data={
            'content': 'This is a test comment',
            'post_id': post.id
        }, follow_redirects=True)
        self.assertIn(b'Your comment has been posted!', response.data)
        comment = Comment.query.filter_by(content='This is a test comment').first()
        self.assertIsNotNone(comment)
   
    def test_follow_unfollow(self):
        self.login('testuser1', 'password')
        user2 = User.query.filter_by(username='testuser2').first()
       
        # Follow
        response = self.client.post(url_for('follow', username='testuser2'), data={}, follow_redirects=True)
        self.assertIn(b'You are following testuser2!', response.data)
        self.assertTrue(User.query.filter_by(username='testuser1').first().is_following(user2))
       
        # Unfollow
        response = self.client.post(url_for('unfollow', username='testuser2'), data={}, follow_redirects=True)
        self.assertIn(b'You are not following testuser2.', response.data)
        self.assertFalse(User.query.filter_by(username='testuser1').first().is_following(user2))
   
    def test_send_message(self):
        self.login('testuser1', 'password')
        response = self.client.post(url_for('send_message', recipient='testuser2'), data={
            'message': 'Hello, testuser2!'
        }, follow_redirects=True)
        self.assertIn(b'Your message has been sent.', response.data)
        message = Message.query.filter_by(body='Hello, testuser2!').first()
        self.assertIsNotNone(message)
   
    def test_translation(self):
        self.login('testuser1', 'password')
        response = self.client.post(url_for('translate_text'), json={
            'text': 'Hello',
            'source_language': 'en',
            'dest_language': 'es'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hola', response.json['text'])
 
    def login(self, username, password):
        return self.client.post(url_for('login'), data={
            'username': username,
            'password': password
        }, follow_redirects=True)
 
if __name__ == '__main__':
    unittest.main()