from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.config import get_db
from app.infraestructure.repositories.client_repository import ClientRepository