from app.infraestructure.repositories.client_repository import ClientRepository

class MessageService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository
        async def process_messsage(self, wa_id:str, name: str, text: str):
            client = await self.repository.get_wa_id(wa_id)
            if not client:
                client = await self.repository.create_client(wa_id, name)
                return f"welcome {name} this is automate message service"
            return f'hi again {client.name}, i get your message {text}'