from sqlalchemy import ForeignKey, Integer, Column, String, DateTime
from sqlalchemy.types import Boolean
from sqlalchemy.sql import func
from config.db import Base


#Esta clase nos permite generar la tabla en la base de datos
class modelDog(Base):
    __tablename__ = 'dogs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    picture = Column(String(255), nullable=False)
    is_adopted = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id',onupdate='cascade'), default=None)
    created_date = Column(DateTime, default=func.now())

    def __init__(self, name, picture, is_adopted, create_date):
        self.name = name
        self.picture = picture
        self.is_adopted = is_adopted
        self.create_date = create_date


