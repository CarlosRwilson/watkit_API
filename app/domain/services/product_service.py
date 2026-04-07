from app.infraestructure.repositories.product_repository import ProductRepository
class ProductService:
    def __init__ (self, repository: ProductRepository):
        self.repository = repository

    async def show_catalog(self) -> str:
            products = await self.repository.get_available_products()
            if not products:
                return "we dont have stock at this moment :("
            
            catalog_msg = "Here is our menu!\n\n"
            for p in products:
                catalog_msg += f"{p.name} (${p.price})\n"
            catalog_msg += "\n to order write *order* "

            return catalog_msg