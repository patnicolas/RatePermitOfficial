__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024  All rights reserved."

from sqlalchemy import Column, Integer, Date, String, ForeignKey
from src.db import Base


class Review(Base):
    __tablename__ = 'reviews'

    """
        Definition of the table for user review/feedback on the building permit application process
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, index=True)
    user_name = Column(String, index=True, nullable=False)
    permit = Column(String, nullable=True)
    comment = Column(String, nullable=False)
    kpi_id = Column(Integer, ForeignKey('kpis.id'))
    permit_official_id = Column(Integer, ForeignKey('permit_officials.id'))