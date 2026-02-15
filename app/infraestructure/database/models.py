from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from datetime import datetime


class Base(DeclarativeBase):
    pass

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    wa_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)#id from Whatsapp
    name: Mapped[str | None] = mapped_column(String(100))
    register_date: Mapped[datetime] = mapped_column(server_default=func.now()) #time created
    last_message: Mapped[datetime | None] = mapped_column(onupdate=func.now())#time updated
    status : Mapped[str] = mapped_column(default="begin")

    
