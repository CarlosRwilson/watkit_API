
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.main import app

from app.domain.services.message_service import MessageService
from app.domain.services.product_service import ProductService

client = TestClient(app)
#Health check 
# Health check endpoint
def test_health():
    response = client.get("/")
    assert response.status_code == 200
@pytest.mark.asyncio
async def test_new_client_greeting():
    client_repo = AsyncMock()
    product_service = AsyncMock()
    order_service = AsyncMock()

    client_repo.get_wa_id.return_value = None
    client_repo.create_client.return_value = type("Client", (), {"id": 1, "first_name": "Carlos"})
    order_service.get_active_order.return_value = None

    service = MessageService(client_repo, product_service, order_service)
    response = await service.process_message(
        wa_id="123",
        first_name="Carlos",
        last_name=None,
        text="hello"
    )
    assert "" in response


@pytest.mark.asyncio
async def test_menu_flow():
    client_repo = AsyncMock()
    order_service = AsyncMock()

    # Mock product repository and service
    product_repo = AsyncMock()
    # mock product with name and price attributes
    product = type("Product", (), {"name": "Pizza", "price": 10.0})
    product_repo.get_available_products = AsyncMock(return_value=[product])
    product_service = ProductService(product_repo)

    # Client in DB
    client_repo.get_wa_id = AsyncMock(return_value=type("Client", (), {"id": 1, "first_name": "Carlos"}))
    order_service.get_active_order = AsyncMock(return_value=None)

    service = MessageService(client_repo, product_service, order_service)
    response = await service.process_message(
        wa_id="123",
        first_name=None,
        last_name="Hankcook",
        text="menu"
    )
    assert "Pizza ($10.0)" in response

@pytest.mark.asyncio
async def test_add_product_to_order():
    client_repo = AsyncMock()
    product_service = AsyncMock()
    order_service = AsyncMock()

    client = type("Client", (), {"id": 1, "first_name": "Carlos"})
    order = type("Order", (), {"id": 99})

    client_repo.get_wa_id.return_value = client
    order_service.get_active_order.return_value = order
    order_service.add_product_to_order.return_value = "Product added"

    service = MessageService(client_repo, product_service, order_service)
    response = await service.process_message(
        wa_id="123",
        text="1"
    )
    assert response == "Product added"