__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024  All rights reserved."

from src.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.db.review import Review


"""
Schema
First name  Str
Last name   Str
Identifier  Optional[Str]
Title       Str
Department  Str
City        Str
Review     List
"""


class PermitOfficial(Base):
    __tablename__ = 'permit_officials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False, index=True)
    identifier = Column(String, nullable=True, index=False)
    title = Column(String, nullable=False)
    department = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    # reviews = relationship('Review', back_populates='permit_officials')
    # Review.group = relationship('PermitOfficial', back_populates='reviews')
