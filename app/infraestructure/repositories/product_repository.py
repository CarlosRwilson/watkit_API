from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infraestructure.database.models import Product

class ProdcutRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

        async def get_product_by_id(self, product_id:int) -> Product | None:
            query = select(Product).where(Product.id == product_id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        async def get_available_products(self):
            query = select(Product).where(Product.stock > 0)
            result = await self.session.execute(query)
            return result.scalars().all()
        
        
        