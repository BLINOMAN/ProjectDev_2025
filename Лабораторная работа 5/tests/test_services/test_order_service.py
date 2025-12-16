import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.main import Order, User, Product
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.services.order_service import OrderService
from app.schemas.order_schemas import OrderCreate


@pytest.mark.asyncio
async def test_order_service_create():
    mock_order_repo = AsyncMock(spec=OrderRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_user_repo = AsyncMock(spec=UserRepository)

    order_service = OrderService(mock_order_repo, mock_product_repo, mock_user_repo)    
    order_data = OrderCreate(user_id="123", product_ids=["456", "789"])

    mock_user = MagicMock(spec=User)
    mock_user_repo.get_by_id.return_value = mock_user 

    mock_product1 = MagicMock(spec=Product)
    mock_product1.stock_quantity = 5  
    mock_product2 = MagicMock(spec=Product)
    mock_product2.stock_quantity = 3  
    
    async def mock_get_product_by_id(product_id):
        if product_id == "456":
            return mock_product1
        elif product_id == "789":
            return mock_product2
        return None

    mock_product_repo.get_by_id = AsyncMock(side_effect=mock_get_product_by_id)  

    mock_order = Order(
        id="abc",
        user_id="123",
        status="pending"
    )
    mock_order_repo.create.return_value = mock_order  
    
    result = await order_service.create(order_data)

    mock_order_repo.create.assert_called_once_with(order_data) 
    
    assert result.user_id == "123"


@pytest.mark.asyncio
async def test_order_service_get_by_id():
    mock_order_repo = AsyncMock(spec=OrderRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_user_repo = AsyncMock(spec=UserRepository)

    order_service = OrderService(mock_order_repo, mock_product_repo, mock_user_repo)

    mock_order = Order(
        id="abc",
        user_id="123",
        status="pending"
    )
    mock_order_repo.get_by_id.return_value = mock_order

    result = await order_service.get_by_id("abc")

    mock_order_repo.get_by_id.assert_called_once_with("abc")  
    assert result.id == "abc"


@pytest.mark.asyncio
async def test_order_service_get_by_id_not_found():
    mock_order_repo = AsyncMock(spec=OrderRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_user_repo = AsyncMock(spec=UserRepository)

    order_service = OrderService(mock_order_repo, mock_product_repo, mock_user_repo)

    mock_order_repo.get_by_id.return_value = None

    result = await order_service.get_by_id("nonexistent")

    mock_order_repo.get_by_id.assert_called_once_with("nonexistent") 
    assert result is None


@pytest.mark.asyncio
async def test_order_service_update_status():
    mock_order_repo = AsyncMock(spec=OrderRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_user_repo = AsyncMock(spec=UserRepository)

    order_service = OrderService(mock_order_repo, mock_product_repo, mock_user_repo)

    existing_order = Order(
        id="abc",
        user_id="123",
        status="pending"
    )
    mock_order_repo.get_by_id.return_value = existing_order

    updated_order = Order(
        id="abc",
        user_id="123",
        status="completed"
    )
    mock_order_repo.update.return_value = updated_order

    result = await order_service.update_status("abc", "completed")

    mock_order_repo.update.assert_called_once_with("abc", "completed")  
    assert result.status == "completed"


@pytest.mark.asyncio
async def test_order_service_delete():
    mock_order_repo = AsyncMock(spec=OrderRepository)
    mock_product_repo = AsyncMock(spec=ProductRepository)
    mock_user_repo = AsyncMock(spec=UserRepository)

    order_service = OrderService(mock_order_repo, mock_product_repo, mock_user_repo)

    mock_order_repo.delete.return_value = True

    result = await order_service.delete("abc")

    mock_order_repo.delete.assert_called_once_with("abc")  
    assert result is True