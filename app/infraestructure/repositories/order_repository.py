from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infraestructure.database.models import Order, OrderItem

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def create_order(self,client_id:int) -> Order:
        new_order = Order(client_id=client_id)
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)
        return new_order
    
    async def add_item(self, order_id: int, product_id:int,
                       quantity: int, price: float) -> OrderItem:
        new_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )
        self.session.add(new_item)
        await self.session.commit()
        return new_item