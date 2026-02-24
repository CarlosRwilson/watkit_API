from app.infraestructure.repositories.client_repository import ClientRepository

class MessageService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository
    async def process_messsage(self, wa_id:str, first_name: str | None=None,
                               last_name:str | None = None, text: str | None=None):
        client = await self.repository.get_wa_id(wa_id)
        if not client:
            client = await self.repository.create_client(
                wa_id=wa_id, 
                first_name=first_name,
                last_name=last_name)
            return f"welcome {first_name} this is automate message service"
        return f'hi again {client.first_name}, i get your message {text}'