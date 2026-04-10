from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infraestructure.database.config import get_db
from app.infraestructure.repositories.client_repository import ClientRepository
from app.infraestructure.repositories.order_repository import OrderRepository
from app.infraestructure.repositories.product_repository import ProductRepository

from app.domain.services.message_service import MessageService
from app.domain.services.product_service import ProductService
from app.domain.services.order_service import OrderService

# Repos
def get_client_repo(db: AsyncSession = Depends(get_db)):
    return ClientRepository(session=db)

def get_product_repo(db: AsyncSession = Depends(get_db)):
    return ProductRepository(session=db)

def get_order_repo(db: AsyncSession = Depends(get_db)):
    return OrderRepository(session=db)


# Services
def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repo),
):
    return ProductService(repository=product_repo)


def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repo),
    product_repo: ProductRepository = Depends(get_product_repo),
):
    return OrderService(order_repo=order_repo, product_repo=product_repo)


def get_message_service(
    client_repo: ClientRepository = Depends(get_client_repo),
    product_service: ProductService = Depends(get_product_service),
    order_service: OrderService = Depends(get_order_service),
):
    return MessageService(
        client_repo=client_repo,
        product_service=product_service,
        order_service=order_service
    )