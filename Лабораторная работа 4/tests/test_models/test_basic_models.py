
"""
Базовые тесты для моделей.
Проверяют, что модели можно создавать и что у них есть нужные атрибуты.
"""

from app.orm.main import User, Product, Order, Address


def test_user_model():
    
    user = User(
        id="123",
        username="Test User",
        email="test@example.com"
    )

    assert user.username == "Test User"
    assert user.email == "test@example.com"
    assert user.id == "123"


def test_product_model():
    
    product = Product(
        id="456",
        name="Test Product",
        description="A product for testing",
        price=100.0,
        stock_quantity=10
    )

    assert product.name == "Test Product"
    assert product.price == 100.0
    assert product.stock_quantity == 10
    assert product.id == "456"


def test_order_model():
    
    order = Order(
        id="789",
        user_id="123",
        status="pending"
    )

    assert order.user_id == "123"
    assert order.status == "pending"
    assert order.id == "789"


def test_address_model():
    
    address = Address(
        id="101",
        user_id="123",
        street="123 Main St",
        city="New York",
        country="USA"
    )

    assert address.street == "123 Main St"
    assert address.city == "New York"
    assert address.country == "USA"
    assert address.user_id == "123"
    assert address.id == "101"