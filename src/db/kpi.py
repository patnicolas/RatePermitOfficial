__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024  All rights reserved."

from src.db import Base
from sqlalchemy import Column, Integer, ForeignKey


class KPI(Base):
    __tablename__ = 'kpis'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    helpfulness = Column(Integer)
    consistency = Column(Integer)
    responsiveness = Column(Integer)
    cost = Column(Integer)