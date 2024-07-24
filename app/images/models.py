from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy_utils.types.url import URLType
from sqlalchemy.orm import relationship
from app.database import Base
from app.posts.models import Posts


class BaseImages:
    id = Column(Integer, primary_key=True)
    url = Column(URLType, nullable=False)

    def __repr__(self):
        return f'Image #{self.id}'


class PostImages(Base, BaseImages):
    __tablename__ = 'post_images'

    post_id = Column(ForeignKey('posts.id'))
    post = relationship('Posts', back_populates='images')


class GroupImages(Base, BaseImages):
    __tablename__ = 'group_images'

    group = relationship('Groups', back_populates='group_image')
    group_id = Column(ForeignKey('groups.id'))