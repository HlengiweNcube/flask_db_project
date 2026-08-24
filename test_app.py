import os
import pytest
from sqlalchemy import select

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import app, db, get_or_create_category
from models import Outfit, Category, User


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        client = app.test_client()
        client.post('/register', data={'username': 'test-user', 'password': 'test-password'})
        yield client
        db.session.remove()
        db.drop_all()


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'African Fashion' in response.data


def test_about_page(test_client):
    response = test_client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data


def test_inventory_requires_login(test_client):
    test_client.post('/logout')
    response = test_client.get('/add')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_add_form_shows_category_dropdown(test_client):
    response = test_client.get('/add')

    assert response.status_code == 200
    assert b'<select id="category" name="category" required>' in response.data
    assert b'<option value="Women">Women</option>' in response.data
    assert b'<option value="Traditional">Traditional</option>' in response.data


def test_add_form_shows_image_dropdown(test_client):
    response = test_client.get('/add')

    assert response.status_code == 200
    assert b'<select id="image_url" name="image_url" required>' in response.data
    assert b'<option value="lobola.jpg">lobola.jpg</option>' in response.data


def test_add_rejects_empty_required_fields(test_client):
    response = test_client.post('/add', data={
        'name': '', 'category': '', 'image_url': '', 'quantity': '', 'price': '',
    })

    assert response.status_code == 400
    assert b'class="form-error"' in response.data
    assert b'Name, category, image, quantity, and price are required.' in response.data


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
        outfit = db.session.scalars(
            select(Outfit).filter_by(name='Test Dress')
        ).first()
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
        updated = db.session.get(Outfit, outfit_id)
        assert updated.name == 'Updated Shirt'
        assert updated.quantity == 3
        assert updated.price == 20.0


def test_category_is_reused_when_outfits_are_added(test_client):
    outfit_data = {
        'category': 'women',
        'description': 'A tested outfit',
        'image_url': 'dress.jpg',
        'quantity': '2',
        'price': '30.00',
    }

    test_client.post('/add', data={**outfit_data, 'name': 'First Dress'})
    test_client.post('/add', data={**outfit_data, 'name': 'Second Dress'})

    with app.app_context():
        assert db.session.scalar(select(Category.id)) is not None
        assert db.session.scalar(select(Category.name)) == 'Women'
        assert db.session.scalar(select(Category.id).where(Category.name == 'Women')) is not None
        assert db.session.scalar(select(Category.id).where(Category.name == 'Women')) == db.session.scalar(
            select(Outfit.category_id).where(Outfit.name == 'First Dress')
        )
        assert len(db.session.scalar(select(Category).where(Category.name == 'Women')).outfits) == 2


def test_api_rejects_invalid_values(test_client):
    response = test_client.post('/api/add-outfit', json={
        'name': 'Invalid Outfit',
        'category': 'Men',
        'image_url': 'shirt.jpg',
        'quantity': -1,
        'price': 20,
    })

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Quantity and price cannot be negative.'


def test_dispatch_reduces_stock(test_client):
    test_client.post('/add', data={
        'name': 'Dispatch Dress', 'category': 'Women', 'image_url': 'dress.jpg',
        'quantity': '5', 'price': '20',
    })

    with app.app_context():
        outfit_id = db.session.scalar(select(Outfit.id).where(Outfit.name == 'Dispatch Dress'))

    response = test_client.post(f'/dispatch/{outfit_id}', data={'amount': '2'})
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Outfit, outfit_id).quantity == 3


def test_delete_removes_outfit(test_client):
    test_client.post('/add', data={
        'name': 'Delete Dress', 'category': 'Women', 'image_url': 'dress.jpg',
        'quantity': '1', 'price': '20',
    })

    with app.app_context():
        outfit_id = db.session.scalar(select(Outfit.id).where(Outfit.name == 'Delete Dress'))

    response = test_client.post(f'/delete/{outfit_id}')
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Outfit, outfit_id) is None
