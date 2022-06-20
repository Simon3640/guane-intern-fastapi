from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship
from config.db import Base

#Esta clase permite generar la tabla en la base de datos
class modelUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    Child = relationship("modelDog", backref="User")
    def __init__(self, name, last_name, email):
        self.name = name
        self.last_name = last_name
        self.email = email
