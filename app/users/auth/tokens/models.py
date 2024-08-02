from sqlalchemy import UUID, Column, ForeignKey, Integer, String, DateTime
from app.database import Base


class RefreshTokens(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(UUID, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, nullable=False)
