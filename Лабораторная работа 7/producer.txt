import asyncio
import json
import random
from aio_pika import connect_robust, Message


RABBITMQ_URL = "amqp://app:app@localhost:5672/local"


async def main():
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    exchange = channel.default_exchange

    print("Отправка 5 сообщений о продукции...")
    for i in range(1, 6):
        product_data = {
            "id": i,
            "name": f"Product {i}",
            "price": round(random.uniform(10.0, 100.0), 2),
            "quantity": random.randint(1, 100)
        }
        message = Message(
            json.dumps(product_data).encode('utf-8'),
            delivery_mode=2,
        )
        await exchange.publish(
            message,
            routing_key='product',
        )
        print(f"  Отправлено: {product_data}")

    print("\nОтправка 3 сообщений о заказах...")
    for i in range(1, 4):
        num_items = random.randint(1, 3)
        items = []
        for _ in range(num_items):
            item_product_id = random.randint(1, 5)
            item_quantity = random.randint(1, min(5, 10))
            items.append({
                "product_id": item_product_id,
                "quantity": item_quantity
            })

        order_data = {
            "id": i,
            "user_id": random.randint(1, 10),
            "items": items,
            "status": "pending"
        }
        message = Message(
            json.dumps(order_data).encode('utf-8'),
            delivery_mode=2,
        )
        await exchange.publish(
            message,
            routing_key='order', 
        )
        print(f"  Отправлено: {order_data}")

    print("\nВсе сообщения отправлены.")

    await connection.close()

if __name__ == "__main__":
    asyncio.run(main())