from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, Enum as SQLAlchemyEnum, ForeignKey, String, Text, Integer, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Attraction(Base):
    __tablename__ = 'attractions'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    image_url = Column(Text)
    address = Column(String(200))
    rating = Column(Float, default=0.0)
    yandex_url = Column(Text)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    image_url = Column(Text)
    address = Column(String(200))
    average_price = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    yandex_url = Column(Text)

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

    def __lt__(self, other):

        order = {Role.USER: 0, Role.ADMIN: 1}
        return order[self] < order.get(other, 0)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(50))
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(SQLAlchemyEnum(Role), default=Role.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    activities = relationship("UserActivity", back_populates="user")

class UserActivity(Base):
    __tablename__ = 'user_activities'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(Text)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="activities")