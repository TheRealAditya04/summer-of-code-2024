import sys
import os
import pytest

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Customer, Staff, InventoryItem, Transaction

@pytest.fixture
def app():
    """Fixture to create and configure the Flask application instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:winterdsoc@localhost/test_myproject'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Fixture to create a test client for the application."""
    return app.test_client()

@pytest.fixture
def init_db(app):
    """Fixture to initialize and clean up the database for each test."""
    with app.app_context():
        db.create_all()  # Create all tables before the test
        yield db
        db.session.remove()
        db.drop_all()  # Drop all tables after the test
