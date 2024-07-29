from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    pub_date = Column(DateTime, nullable=False)
    vk_id = Column(Integer, nullable=False, unique=True)
    text = Column(Text)
    images = relationship('PostImages', back_populates='post', lazy='selectin')
    group = relationship('Groups', back_populates='posts', lazy='joined')
    group_id = Column(Integer, ForeignKey('groups.id'))

    def __repr__(self):
        return f'Post #{self.id}'