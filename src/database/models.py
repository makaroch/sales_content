from enum import Enum

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Date, Time, func, BINARY, TEXT


class Status(Enum):
    FREE = 'FREE'
    RASS = 'RASS'


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(255))
    is_paid_cheap_content = Column(Boolean, default=False)
    is_paid_expensive_content = Column(Boolean, default=False)
    date_create = Column(Date, server_default=func.current_date())
    date_paid = Column(Date, nullable=True, default=None)
    # time_paid = Column(Time, nullable=True, default=None)

    def __str__(self):
        return f"Клиент: {self.username} | {self.id} | {self.is_paid}"


class BinaryDocument(Base):
    __tablename__ = "documents"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(255))
    expansion = Column(String(10))
    status_file = Column(String(10))
    file_data = Column(BINARY)


class PaySettings(Base):
    __tablename__ = "pay_settings"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    message = Column(TEXT)
    btn_text = Column(String(255))
    price = Column(Integer)
    url = Column(String(255))
    user_friendly_id = Column(Integer)
    id_chanel = Column(Integer)


class HelloMessage(Base):
    __tablename__ = "hello_message"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    message = Column(TEXT)
    user_friendly_id = Column(Integer)


class HelpChat(Base):
    __tablename__ = "help_chat"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    message = Column(TEXT)
    user_friendly_id = Column(Integer)
