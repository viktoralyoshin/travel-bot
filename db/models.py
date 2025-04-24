from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Attraction(Base):
    __tablename__ = 'attractions'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    image_url = Column(Text)
    address = Column(String(200))
    rating = Column(Integer, default=0)
    yandex_url = Column(Text)

    def __repr__(self):
        return f"<Attraction {self.name}>"