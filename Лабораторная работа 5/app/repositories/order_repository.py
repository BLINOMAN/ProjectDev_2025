
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.orm.main import Order, Product, order_product
from app.schemas.order_schemas import OrderCreate


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        result = await self.session.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.products))
        )
        return result.scalar_one_or_none()

    async def create(self, order_data: OrderCreate) -> Order:
        product_ids = order_data.product_ids
        products = await self.session.execute(select(Product).where(Product.id.in_(product_ids)))
        products = products.scalars().all()

        if len(products) != len(product_ids):
            missing = set(product_ids) - {p.id for p in products}
            raise ValueError(f"Products not found: {missing}")

        
        for product in products:
            if product.stock_quantity < 1:
                raise ValueError(f"Product {product.name} is out of stock")

        order = Order(user_id=order_data.user_id, status="pending")
        self.session.add(order)
        await self.session.flush()  

        for product_id in product_ids:
            await self.session.execute(
                insert(order_product).values(order_id=order.id, product_id=product_id, quantity=1)
            )

        for product in products:
            product.stock_quantity -= 1

        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def update(self, order_id: str, status: str) -> Optional[Order]:
        order = await self.get_by_id(order_id)
        if not order:
            return None
        order.status = status
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def delete(self, order_id: str) -> bool:
        order = await self.get_by_id(order_id)
        if not order:
            return False
        await self.session.delete(order)
        await self.session.commit()
        return True

    async def get_total_count(self) -> int:
        result = await self.session.execute(select(Order))
        return len(result.scalars().all())

    async def get_all(self, count: int = 10, page: int = 1) -> List[Order]:
        offset = (page - 1) * count
        result = await self.session.execute(
            select(Order)
            .offset(offset)
            .limit(count)
            .options(selectinload(Order.products))  
        )
        return result.scalars().all()