from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.infraestructure.database.models import Order, OrderItem, OrderStatus
from sqlalchemy.orm import selectinload

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def create_order(self,client_id:int) -> Order:
        new_order = Order(client_id=client_id,status=OrderStatus.ORDERING)
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
            price_at_time=price
        )
        self.session.add(new_item)
        await self.session.commit()
        return new_item
    
    async def get_order_by_status(self,client_id: int, status:OrderStatus) -> Order | None:
        query = (
            select(Order).where(
            Order.client_id == client_id,
            Order.status == status)
            .options(selectinload(Order.items))
            
            )
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def update_order_status(self, order_id: int, new_status: OrderStatus):
        query = update(Order).where(Order.id == order_id).values(status=new_status)
        await self.session.execute(query)
        await self.session.commit()