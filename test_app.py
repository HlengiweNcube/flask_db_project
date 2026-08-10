import pytest

from app import app, db, get_or_create_category
from models import Outfit, Category


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'African Fashion' in response.data


def test_add_outfit(test_client):
    response = test_client.post(
        '/add',
        data={
            'name': 'Test Dress',
            'category': 'Women',
            'description': 'Test description',
            'image_url': 'test.jpg',
            'quantity': '5',
            'price': '25.00'
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'Test Dress' in response.data

    with app.app_context():
        outfit = Outfit.query.filter_by(name='Test Dress').first()
        assert outfit is not None
        assert outfit.category.name == 'Women'
        assert outfit.quantity == 5


def test_edit_outfit(test_client):
    with app.app_context():
        category = get_or_create_category('Men')
        outfit = Outfit(
            name='Test Shirt',
            description='A shirt for testing',
            image_url='shirt.jpg',
            quantity=2,
            price=15.0,
            category=category
        )
        db.session.add(outfit)
        db.session.commit()
        outfit_id = outfit.id

    response = test_client.post(
        f'/edit/{outfit_id}',
        data={
            'name': 'Updated Shirt',
            'category': 'Men',
            'description': 'Updated description',
            'image_url': 'shirt2.jpg',
            'quantity': '3',
            'price': '20.00'
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        updated = Outfit.query.get(outfit_id)
        assert updated.name == 'Updated Shirt'
        assert updated.quantity == 3
        assert updated.price == 20.0
