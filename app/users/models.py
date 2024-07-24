from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'User #{self.id}'
    