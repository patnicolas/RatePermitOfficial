__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024  All rights reserved."

from src.db import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey, LargeBinary


class User(Base):
    __tablename__ = 'users'
    """
        Definition of the table for users (see Role for roles)
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, index=True, nullable=False)
    created = Column(Date, index=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    is_anonymous = Column(Integer)
    credential = Column('password', LargeBinary, nullable=False)        # Needs to be encrypted

