__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024  All rights reserved."

from src.db import Base
from sqlalchemy import Column, Integer, Date, String


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    is_active = Column(Integer)


