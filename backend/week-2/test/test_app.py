import pytest
from app import create_app, db
from app.models import InventoryItem

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_add_product(client):
    response = client.post('/products/add', data={
        'name': 'Test Product',
        'description': 'Test Description',
        'price': 10.5,
        'quantity': 5
    })
    assert b'Product added successfully!' in response.data

def test_list_products(client):
    client.post('/products/add', data={
        'name': 'Test Product',
        'description': 'Test Description',
        'price': 10.5,
        'quantity': 5
    })
    response = client.get('/products')
    assert b'Test Product' in response.data
