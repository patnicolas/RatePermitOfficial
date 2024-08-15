

_author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from pydantic import BaseModel
from typing import AnyStr

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
