import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple
import enum

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.db.query_cache import QueryCache

from bs4 import BeautifulSoup

queries = QueryCache(Path(__file__).parent / "queries")

################################################################################################
#                                        Types                                                 #
################################################################################################

@dataclass
class Debate:
    id: int
    title: str
    debate_type: str
    html: BeautifulSoup

VoteType = enum.Enum("VoteType", "PARTY CONSCIENCE")
VoteChoice = enum.Enum("VoteChoice", "AYE NAY")

@dataclass
class Vote:
    voter: str
    num_votes: int
    choice: VoteChoice

class VoteParseError(Exception):
    pass

################################################################################################
#                             Extracting data for party votes                                  #
################################################################################################

def get_vote_choice(choice_text: str):
    if choice_text == "Ayes":
        return VoteChoice.AYE
    elif choice_text == "Noes":
        return VoteChoice.NAY
    else:
        raise VoteParseError(f"Invalid vote choice: {choice_text}")

def get_voters_and_numbers(voters_text: str) -> List[Tuple[str, int]]:
    votes = []
    for party_vote in voters_text.split(';'):
        parts = party_vote.split()
        count = int(parts[-1].strip('.'))
        party = " ".join(parts[:-1])
        votes.append((party, count))
    return votes

def process_party_votes(total_count: str, voter_text: str) -> List[Vote]:

    [choice_text, count_text] = total_count.split()
    choice = get_vote_choice(choice_text)
    total = int(count_text)

    votes = get_voters_and_numbers(voter_text) 
    votes = [Vote(vote[0], vote[1], choice) for vote in votes]

    try:
        validate_parties([vote.voter for vote in votes])
        validate_total(total, votes)
    except VoteParseError as err:
        raise VoteParseError(f"Votes: {votes}") from err 

    return votes

# This function relies on the presence of the .VoteCount and .VoteText elements in the html 
# Where VoteCount containes the total number of votes for or against e.g. Aye 21
# and VoteText contains information about the partis seperated by semicolons e.g. New Zealand Labour 31; ...
def parse_debate(debate: Debate) -> Tuple[VoteType, List[Vote]]:
    vote_total_lines = [line.text for line in debate.html.find_all("p", {"class": "VoteCount"})]
    voters_lines = [line.text for line in debate.html.find_all("p", {"class": "VoteText"})]

    try:
        assert len(vote_total_lines) == len(voters_lines), "Found different numbers of total votes and voter information"
        assert len(vote_total_lines) != 0, "Did not find any lines of vote information"

        vote_list = []
        for count, voters in zip(vote_total_lines, voters_lines):
                vote_list += process_party_votes(count, voters)

    except Exception as err:
        raise Exception(f"Error processing {debate.title}") from err

    return VoteType.PARTY, vote_list   

################################################################################################
#                                        Utilities                                             #
################################################################################################

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

################################################################################################
#                                    Validators                                                #
################################################################################################

def validate_parties(parties: List[str]):
    expected_parties = ["New Zealand Labour", "Green Party of Aotearoa New Zealand", "Te Paati Māori",
               "New Zealand National", "ACT New Zealand"]

    for party in parties:
        if party not in expected_parties:
            raise VoteParseError(f"Invalid party name: {party}")

def validate_total(expected_total: int, votes: List[Vote]):
    actual_total = sum([vote.num_votes for vote in votes])
    
    if actual_total != expected_total:
        raise VoteParseError(f"Total votes is: {actual_total}, expected: {expected_total}")
