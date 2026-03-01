from app.infraestructure.repositories.order_repository import OrderRepository
from app.infraestructure.repositories.product_repository import ProductRepository
from app.infraestructure.database.models import OrderStatus, Order
class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo : ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def start_new_order(self, client_id: int ) -> str:
            order = await self.order_repo.create_order(
                    client_id=client_id
                    )
            return f"Order #{order.id} done!, which product you want to add? (send the ID)"
    async def add_product_to_order(self, order_id: int, product_id: int, quantity: int = 1) -> str: 
            #product exist?
            product = await self.product_repo.get_product_by_id(product_id)

            if not product:
                return "invalid product ID. Please Check the menu"
            
            if product.stock < quantity:
                return f"we only have {product.stock} units of {product.name}"
            
            await self.order_repo.add_item(
                order_id=order_id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            await self.product_repo.decrease_stock(product.id, quantity)
            return (
                 f'{quantity} x {product.name} added!\n\n '
                 'Want to add another product? Send the *ID*\n'
                 'If you are done, write *checkout* to finish your order'
            )
    async def get_active_order(self, client_id:int) -> Order | None:
         return await self.order_repo.get_order_by_status(
              client_id=client_id,
              status=OrderStatus.ORDERING
         )
# app/domain/services/order_service.py

    async def checkout(self, client_id: int) -> str:
        order = await self.order_repo.get_order_by_status(client_id, OrderStatus.ORDERING)
        
        if not order or not order.items:
            return "You don't have an active order or your cart is empty."
    
        total = sum(item.quantity * item.price_at_time for item in order.items)
        
    
        await self.order_repo.update_order_status(order.id, OrderStatus.PAID)
        
        return (
            f"*Order Confirmed!*\n\n"
            f"Order ID: #{order.id}\n"
            f"Total to pay: ${total:.2f}\n\n"
            "Thank you for your purchase! We are preparing your order."
        )