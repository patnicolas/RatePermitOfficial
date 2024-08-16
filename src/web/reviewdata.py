__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from pydantic import BaseModel
from typing import AnyStr


"""
Class that is used by HTTP post for reviews
permitofficial: Last name of Building permit official
permit: Permit number if available
helpfulness: Helpfulness KPI [1, 5]
consistency: Consistency KPI [1, 5]
responsiveness: Responsiveness KPI [1, 5]
cost: Cost KPI [1, 5]
comment: Comments, feedback from users
"""


class ReviewData(BaseModel):
    permitofficial: str
    permit: str
    helpfulness: int
    consistency: int
    responsiveness: int
    cost: int
    comment: str

    def __str__(self) -> AnyStr:
        return f'\nOfficial: {self.permitofficial}' \
               f'\nHelpfulness: {self.helpfulness}' \
               f'\nConsistency: {self.consistency}' \
               f'\nResponsiveness:  {self.responsiveness}' \
               f'\nConst:  {self.cost}' \
               f'\nComments:\n {self.comment[0: 64]}... '
