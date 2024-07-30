from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy_utils.types.url import URLType
from sqlalchemy.orm import relationship
from app.database import Base
from app.posts.models import Posts


class BaseImages:
    id = Column(Integer, primary_key=True)
    url = Column(URLType, nullable=False)


class PostImages(Base, BaseImages):
    __tablename__ = 'post_images'

    post_id = Column(ForeignKey('posts.id'))
    post = relationship('Posts', back_populates='images', lazy='joined')

    def __repr__(self):
        return f'<Post image #{self.id}>'


class GroupImages(Base, BaseImages):
    __tablename__ = 'group_images'

    group = relationship('Groups', back_populates='group_image', lazy='joined')
    group_id = Column(ForeignKey('groups.id'))

    def __repr__(self):
        return f'<Group image #{self.id}>'