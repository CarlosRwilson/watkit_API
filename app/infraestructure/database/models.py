from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import String, DateTime, func, ForeignKey
from datetime import datetime
from typing import List
from sqlalchemy import Float, Text, Boolean


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
    #foregein key to connect to enterprise
    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"))
    enterprise: Mapped["Enterprise"] = relationship(back_populates="clients")


class Enterprise(Base):
    __tablename__ = "enterprises"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    api_key: Mapped[str] = mapped_column(String(100), unique=True) 
    whatsapp_number: Mapped[str] = mapped_column(String(100), unique=True)

    #one enterprise has a lot of clients
    clients: Mapped[list["Client"]] = relationship(back_populates="enterprise")

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    description : Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float(10,00))
    #default true if Product exist, otherwise change to false
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"))
    enterprise: Mapped["Enterprise"] = relationship(back_populates="products")
