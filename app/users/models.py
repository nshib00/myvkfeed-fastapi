from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    vk_shortname = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    date_joined = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f'User #{self.id}'
    