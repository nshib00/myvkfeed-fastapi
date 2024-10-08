from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Groups(Base):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, nullable=False, unique=True)
    title = Column(String, nullable=False)
    is_hidden = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_image = relationship(
        'GroupImages',
        back_populates='group',
        uselist=False,
        lazy='joined',
        cascade='all, delete-orphan',
    )
    posts = relationship(
        'Posts',
        back_populates='group',
        lazy='selectin',
        cascade='all, delete',
    )

    def __repr__(self):
        return f'<Group "{self.title}">'