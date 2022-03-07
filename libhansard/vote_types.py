import enum
from dataclasses import dataclass

VoteType = enum.Enum("VoteType", "PARTY CONSCIENCE")
VoteChoice = enum.Enum("VoteChoice", "AYE NAY")

@dataclass
class Vote:
    voter: str
    num_votes: int
    choice: VoteChoice
    vote_type: VoteType
