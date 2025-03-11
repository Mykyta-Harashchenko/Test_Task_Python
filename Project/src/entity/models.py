import enum
from sqlalchemy import Integer, String, Date, Boolean, Text, ForeignKey, DateTime, func, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    messages = relationship("Message", back_populates="sender", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    request: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    sender = relationship("User", back_populates="messages")

