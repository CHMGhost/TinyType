import pytest
from app import app, db, Post
import os


# Fetch admin credentials
ADMIN_USERNAME = os.getenv('FLASK_ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.getenv('FLASK_ADMIN_PASSWORD_HASH')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_home_page(client):
    """Test if the home page loads correctly"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'My Blog' in rv.data

def test_login_page(client):
    """Test if the login page loads correctly"""
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b'Login' in rv.data

def test_create_post():
    """Test post creation"""
    post = Post(
        title='Test Post',
        content='Test Content',
        user_id=1
    )
    assert post.title == 'Test Post'
    assert post.content == 'Test Content'