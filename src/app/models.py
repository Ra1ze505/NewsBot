from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from config.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    key = relationship("UserKey", back_populates="user")
