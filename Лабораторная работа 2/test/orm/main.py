from sqlalchemy.orm import *
from sqlalchemy import ForeignKey, func

from datetime import datetime
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    description: Mapped[str] = mapped_column(default='No description')

    addresses = relationship('Address', back_populates='user')
    orders = relationship('Order', back_populates='user')


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=True)
    zip_code: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='addresses')
    orders = relationship('Order', back_populates='address')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False, default='No description')
    price: Mapped[float] = mapped_column(nullable=False)
    
    orders = relationship('Order', back_populates='product')

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    address_id: Mapped[UUID] = mapped_column(ForeignKey('addresses.id'), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'), nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='orders')
    address = relationship('Address', back_populates='orders')
    product = relationship('Product', back_populates='orders')