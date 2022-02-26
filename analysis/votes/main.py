import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple
import enum

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.db.db import get_db 
from libhansard.db.query_cache import QueryCache

from bs4 import BeautifulSoup

@dataclass
class Debate:
    id: int
    title: str
    debate_type: str
    html: BeautifulSoup

VoteType = enum.Enum("VoteType", "PARTY CONSCIENCE")
VoteChoice = enum.Enum("VoteChoice", "AYE NAY")

# Make this structure better
@dataclass
class DebateVote:
    vote_type: VoteType
    votes: List[Tuple[str, int, VoteChoice]]


queries = QueryCache(Path(__file__).parent / "queries")

# TODO look into pycopg data factories
def get_debates_by_type(debate_type: str, conn) -> List[Debate]:
    with conn.cursor() as cur:
        cur.execute(queries.get_query("get_debate_by_type"), (debate_type,))
        debate_rows = cur.fetchall()

        debates = [
            Debate(
                id = row[0],
                title = row[1],
                debate_type = debate_type,
                html = BeautifulSoup(row[2], "html.parser"),
            ) for row in debate_rows]
        return debates

# Count represents the decision and the number of votes e.g. 'Ayes 85'
def process_party_votes(total_count: str, text: str) -> List[DebateVote]:
    votes = []
    choice = None 
    
    # Process count 
    [choice_text, count_text] = total_count.split()
    if choice_text == "Ayes":
        choice = VoteChoice.AYE
    elif choice_text == "Noes":
        choice = VoteChoice.NAY
    elif choice == None:
        raise ValueError(f"Invalid vote choice: {choice_text}")

    total = int(count_text)

    for party_vote in text.split(';'):
        parts = party_vote.split()
        count = int(parts[-1].strip('.'))
        party = " ".join(parts[:-1])

        # TODO add assert for party names
        vote = DebateVote(VoteType.PARTY, (party, count, choice))  # type: ignore
        votes.append(vote)

    # TODO assert totals match

    return votes



def parse_debate(debate: Debate) -> Optional[DebateVote]:
    vote_totals = debate.html.find_all("p", {"class": "VoteCount"})
    vote_texts = debate.html.find_all("p", {"class": "VoteText"})

    vote_list = []
    for count_elem, text_elem in zip(vote_totals, vote_texts):
        count = count_elem.text
        text = text_elem.text
        try:
            vote_list += process_party_votes(count, text)
        except ValueError as err:
            print(err)
            print(f"When processing Debate: {debate.title}")
            sys.exit(1)

    return vote_list   # type: ignore 


