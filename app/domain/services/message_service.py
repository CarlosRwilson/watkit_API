from app.infraestructure.repositories.client_repository import ClientRepository
from app.domain.services.product_service import ProductService
from app.domain.services.order_service import OrderService
from app.infraestructure.database.models import OrderStatus
class MessageService:
    def __init__(self, client_repo: ClientRepository, product_service: ProductService, order_service: OrderService):
        self.client_repo = client_repo
        self.product_service = product_service
        self.order_service = order_service
    
    async def process_message(self, wa_id:str, first_name: str | None=None,
                               last_name:str | None = None, text: str | None=None) -> str:
        client = await self.client_repo.get_wa_id(wa_id)
        if not client:
            client = await self.client_repo.create_client(
                wa_id=wa_id, 
                first_name=first_name,
                last_name=last_name)
            greeting = f"welcome {first_name}! this is our automate service "
        else:
            greeting = f"Hi again {client.first_name}, i hope you are great!"
        user_text = text.lower().strip() if text else ""

        active_order = await self.order_service.get_active_order(client.id)

        if active_order and user_text.isdigit():
            product_id = int(user_text)

            response = await self.order_service.add_product_to_order(
                order_id=active_order.id,
                product_id=product_id
            )
            return response



        if user_text in ['hour', 'hours', 'schedule']:
            return f"{greeting}Our hours to order is 24/7.If you want to order see our *menu*.\n write 'menu'"

        elif user_text in ['price', 'prices', 'costs']:
            return f"{greeting}We have different prices.\nWrite 'menu' if you want to see the menu"
        
        elif user_text in ['checkout']:
            response = await self.order_service.checkout(client.id)
            return response

        elif user_text in ['menu']:
            catalog = await self.product_service.show_catalog()


            if not active_order:
                order_msg = await self.order_service.start_new_order(client.id)
            else:
                order_msg = "you already have an active order.Send the product ID"
            # update status
            return f"{catalog}\n\n{order_msg}"
        else:
            return f'{greeting}Please, write one of this words:\n*Menu*\n*Hour*\n*Price*'
        
