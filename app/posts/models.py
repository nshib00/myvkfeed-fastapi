from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    pub_date = Column(DateTime, nullable=False)
    group_id = Column(ForeignKey('groups.id'))
    text = Column(Text)
    images = relationship('PostImages', back_populates='post')

    def __repr__(self):
        return f'Post #{self.id}'