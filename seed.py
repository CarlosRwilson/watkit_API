import asyncio
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.infraestructure.database.config import DATABASE_URL
from app.infraestructure.database.models import Product


DATA_PRODUCTS = [
    {"name": "Espresso", "price": 2.50, "stock": 50},
    {"name": "Cappuccino", "price": 3.75, "stock": 30},
    {"name": "Latte Machiatto", "price": 4.25, "stock": 25},
    {"name": "Cheese Burger", "price": 8.50, "stock": 15},
    {"name": "Classic Pizza", "price": 12.00, "stock": 10},
    {"name": "Club Sandwich", "price": 7.50, "stock": 20},
    {"name": "Chocolate Muffin", "price": 3.00, "stock": 40},
    {"name": "Green Tea", "price": 2.80, "stock": 60},
    {"name": "Coca Cola 500ml", "price": 2.00, "stock": 100},
    {"name": "French Fries", "price": 4.50, "stock": 35},
]

async def seed_data():
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            print("injecting products to the data base...")

            for p_data in DATA_PRODUCTS:
                new_product = Product(
                    name=p_data['name'],
                    price=p_data['price'],
                    stock=p_data['stock']
                )
                session.add(new_product)
                print('...')
            await session.commit()
            print('products saved succesfully!')

    except Exception as e:
        print(f'error {e}')
    finally:
        print('process done')


#we use this in development not in production

if __name__ == '__main__':
    asyncio.run(seed_data())
    