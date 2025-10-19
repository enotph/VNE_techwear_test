import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_product():
    product_data = {
        'name': 'Test Jacket',
        'description': 'Waterproof urban jacket',
        'price': 299.99,
        'category': 'Jackets',
        'sizes': ['S', 'M', 'L']
    }

    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == product_data['name']
    assert data['price'] == product_data['price']
    assert 'id' in data


def test_get_products():
    client.post('/products', json={
        'name': 'Test Product',
        'price': 100,
        'category': 'Test'
    })

    response = client.get('/products')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_product_not_found():
    response = client.get('/products/999')
    assert response.status_code == 404