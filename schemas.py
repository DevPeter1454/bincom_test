from pydantic import BaseModel,ValidationError, validator
from typing import List

class PartyResult(BaseModel):
    party_abbreviation: str
    party_score: int

class NewPollingUnitResult(BaseModel):
    polling_unit_uniqueid: int
    party_results: List[PartyResult]
    user_name: str

    @validator("party_results", each_item=True)
    def check_party_score(cls, v):
        if v.party_score < 0:
            raise ValueError("Party score must be a non-negative integer")
        return v